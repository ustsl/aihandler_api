from src.modules.gpt.modules.param import (
    model_price,
    dalee_quality,
    dalee_size,
)


class GptTokenCalculator:
    def __init__(self, model, value):
        self._model = model
        self._value = value
        self._model_price = model_price
        self.price_per_unit = self._get_price_for_model()

    def _get_price_for_model(self):
        default_price = 0.08
        return self._model_price.get(self._model, default_price)

    def calc(self):
        total_cost = (self._value / 1000) * self.price_per_unit
        return total_cost


class GptImageCalculator:
    def __init__(self, quality, size):
        self._model = "dall-e-3"
        self._quality = quality
        self._size = size
        self._model_price = model_price
        self._dalee_quality = dalee_quality
        self._dalee_size = dalee_size

    def calc(self):
        price = self._model_price.get(self._model)
        if self._dalee_quality.get(self._quality):
            price += self._dalee_quality.get(self._quality)
        if self._dalee_size.get(self._size):
            price += self._dalee_size.get(self._size)
        return round(price, 2)
