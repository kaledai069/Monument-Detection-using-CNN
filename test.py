import tensorflow as tf
from utils import bbox_utils, data_utils, drawing_utils, io_utils, train_utils, eval_utils
from models.decoder import get_decoder_model
from helper import label_generator

from models.ssd_mobilenet_v2 import get_model, init_model

args = io_utils.handle_args()
backbone = args.backbone
hyper_params = train_utils.get_hyper_params(backbone)

# test_data, size_info = data_utils.get_dataset("test")
# total_items = size_info

labels = label_generator.csv_to_label_map(args.label_path, 'list-type')
labels = ["bg"] + labels
hyper_params["total_labels"] = len(labels)
img_size = hyper_params["img_size"]

data_types = data_utils.get_data_types()
data_shapes = data_utils.get_data_shapes()
padding_values = data_utils.get_padding_values()

# if use_custom_images:
#     img_paths = data_utils.get_custom_imgs(custom_image_path)
#     total_items = len(img_paths)
#     test_data = tf.data.Dataset.from_generator(lambda: data_utils.custom_data_generator(
#                                                img_paths, img_size, img_size), data_types, data_shapes)
# else:
#     test_data = test_data.map(lambda x : data_utils.preprocessing(x, img_size, img_size))

# test_data = test_data.padded_batch(batch_size, padded_shapes=data_shapes, padding_values=padding_values)

ssd_model = get_model(hyper_params)
ssd_model_path = io_utils.get_model_path(backbone)
ssd_model.load_weights(ssd_model_path)


prior_boxes = bbox_utils.generate_prior_boxes(hyper_params["feature_map_shapes"], hyper_params["aspect_ratios"])
ssd_decoder_model = get_decoder_model(ssd_model, prior_boxes, hyper_params)



# step_size = train_utils.get_step_size(total_items, batch_size)
# pred_bboxes, pred_labels, pred_scores = ssd_decoder_model.predict(test_data, steps=step_size, verbose=1)

# if evaluate:
#     eval_utils.evaluate_predictions(test_data, pred_bboxes, pred_labels, pred_scores, labels, batch_size)
# else:
#     drawing_utils.draw_predictions(test_data, pred_bboxes, pred_labels, pred_scores, labels, batch_size)