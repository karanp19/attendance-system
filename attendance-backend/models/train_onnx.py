"""
ONNX Training Script - Generate placeholder model
"""

import onnx
import onnxruntime as ort
import numpy as np

def create_siamone_model(model_path: str = 'models/siamone.onnx'):
    """
    Create a simple Siamese Network ONNX model for testing
    """
    
    # Create graph structure
    nodes = [
        # Convolution layers
        ('conv1', 'input', 'filters', 'features1'),
        ('conv2', 'features1', 'filters', 'features2'),
        # Pooling layers
        ('pool1', 'features1', 'emb1'),
        ('pool2', 'features2', 'emb2'),
        # Distance computation
        ('dist', 'emb1', 'emb2', 'embedding_distance'),
    ]
    
    # Inputs and outputs
    inputs = ['input']
    outputs = ['embedding_distance']
    
    # Inputs and outputs types
    input_type = onnx.TensorProto.FLOAT
    output_type = onnx.TensorProto.FLOAT
    
    # Create ONNX graph
    graph = onnx.make_graph(
        nodes=nodes,
        inputs=inputs,
        outputs=outputs,
        value_info=[
            (onnx.helper.make_tensor_value_info('input', input_type, [1, 3, 128, 128])),
            (onnx.helper.make_tensor_value_info('filters', input_type, [1, 64, 3, 3])),
            (onnx.helper.make_tensor_value_info('features1', input_type, [1, 64, 128, 128])),
            (onnx.helper.make_tensor_value_info('features2', input_type, [1, 64, 128, 128])),
            (onnx.helper.make_tensor_value_info('emb1', input_type, [1, 512])),
            (onnx.helper.make_tensor_value_info('emb2', input_type, [1, 512])),
        ]
    )
    
    dummy_model = onnx.GraphProto()
    dummy_model.SetAttributes(graph)
    
    # Save model
    onnx.save(dummy_model, model_path)
    
    print(f"Created ONNX model at {model_path}")
    return model_path

if __name__ == "__main__":
    model_path = create_siamone_model()
    print(f"Model ready at: {model_path}")