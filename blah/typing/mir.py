from typing import Any, TypeAlias

import numpy
import numpy.typing

WordClass: TypeAlias = Any
SpeechFeatures: TypeAlias = numpy.typing.NDArray[numpy.float32]
EmbeddingsVector: TypeAlias = list[float]
