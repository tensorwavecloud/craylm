from typing import Iterable, List, Optional, Tuple, Union

import torch
from torch import nn

from vllm.attention import AttentionMetadata
from vllm.model_executor.layers.pooler import Pooler, PoolingType
from vllm.model_executor.pooling_metadata import PoolingMetadata
from vllm.sequence import IntermediateTensors, PoolerOutput

from .gemma2 import Gemma2Model
from .interfaces import SupportsPP


class Gemma2EmbeddingModel(nn.Module, SupportsPP):
    """A model that uses Gemma2 with additional embedding functionalities.

    This class encapsulates the Gemma2Model and provides an interface for
    embedding operations and customized pooling functions.

    Attributes:
        model: An instance of Gemma2Model used for forward operations.
        _pooler: An instance of Pooler used for pooling operations.
    """

    def __init__(
        self,
        **kwargs,
    ) -> None:
        super().__init__()
        self.model = Gemma2Model(**kwargs)
        self._pooler = Pooler(pooling_type=PoolingType.LAST, normalize=True)

        self.make_empty_intermediate_tensors = (
            self.model.make_empty_intermediate_tensors
        )

    def forward(
        self,
        input_ids: Optional[torch.Tensor],
        positions: torch.Tensor,
        kv_caches: List[torch.Tensor],
        attn_metadata: AttentionMetadata,
        intermediate_tensors: Optional[IntermediateTensors] = None,
        inputs_embeds: Optional[torch.Tensor] = None,
    ) -> Union[torch.Tensor, IntermediateTensors]:
        return self.model(
            input_ids,
            positions,
            kv_caches,
            attn_metadata,
            intermediate_tensors,
            inputs_embeds,
        )

    def pooler(
        self,
        hidden_states: torch.Tensor,
        pooling_metadata: PoolingMetadata,
    ) -> Optional[PoolerOutput]:
        return self._pooler(hidden_states, pooling_metadata)

    def load_weights(self, weights: Iterable[Tuple[str, torch.Tensor]]):
        self.model.load_weights(weights)
