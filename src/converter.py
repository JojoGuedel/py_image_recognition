from typing import List
from typing import Any
from dataclasses import dataclass
import json
@dataclass
class Metadata:
    height: int
    width: int
    format: str

    @staticmethod
    def from_dict(obj: Any) -> 'Metadata':
        _height = int(obj.get("height"))
        _width = int(obj.get("width"))
        _format = str(obj.get("format"))
        return Metadata(_height, _width, _format)

@dataclass
class Rectangle:
    x: int
    y: int
    w: int
    h: int

    @staticmethod
    def from_dict(obj: Any) -> 'Rectangle':
        _x = int(obj.get("x"))
        _y = int(obj.get("y"))
        _w = int(obj.get("w"))
        _h = int(obj.get("h"))
        return Rectangle(_x, _y, _w, _h)

@dataclass
class Object:
    rectangle: Rectangle
    object: str
    confidence: float

    @staticmethod
    def from_dict(obj: Any) -> 'Object':
        _rectangle = Rectangle.from_dict(obj.get("rectangle"))
        _object = str(obj.get("object"))
        _confidence = float(obj.get("confidence"))
        return Object(_rectangle, _object, _confidence)

@dataclass
class Root:
    objects: List[Object]
    requestId: str
    metadata: Metadata

    @staticmethod
    def from_dict(obj: Any) -> 'Root':
        _objects = [Object.from_dict(y) for y in obj.get("objects")]
        _requestId = str(obj.get("requestId"))
        _metadata = Metadata.from_dict(obj.get("metadata"))
        return Root(_objects, _requestId, _metadata)

# Example Usage
# jsonstring = json.loads(myjsonstring)
# root = Root.from_dict(jsonstring)
