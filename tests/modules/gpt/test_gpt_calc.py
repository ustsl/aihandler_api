from src.modules.gpt.modules.calc import GptImageCalculator, GptTokenCalculator


async def test_gpt_token_calc():

    calculator = GptTokenCalculator(model="gpt-3.5-turbo", value=1000)
    price = calculator.calc()
    assert price == 0.045
    calculator = GptTokenCalculator(model="gpt-4-turbo", value=1000)
    price = calculator.calc()
    assert price == 0.075
    calculator = GptTokenCalculator(model="gpt-4o", value=1000)
    price = calculator.calc()
    assert price == 0.12
    calculator = GptTokenCalculator(model="gpt-4o-mini", value=1000)
    price = calculator.calc()
    assert price == 0.03


async def test_gpt_image_calc():

    calculator = GptImageCalculator(size=None, quality=None)
    price = calculator.calc()
    assert price == 0.23
    calculator = GptImageCalculator(size="1024x1024", quality=None)
    price = calculator.calc()
    assert price == 0.23
    calculator = GptImageCalculator(size="1792x1024", quality=None)
    price = calculator.calc()
    assert price == 0.3
    calculator = GptImageCalculator(size="1792x1024", quality="hd")
    price = calculator.calc()
    assert price == 0.38
