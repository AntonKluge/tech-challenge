import numpy as np

from lens_gpt_backend.producer.producer import Producer
from lens_gpt_backend.utils.product import Product


class PriceProducer(Producer):

    def _produce(self, input_value: Product) -> tuple[Product, bool]:
        items: list[dict[str, str | None]] = [price_dict.get_dict_str_str() for price_dict in input_value.get_list()]

        used_prices = [float(item['price']) for item in items if item['wear'] == 'Pre-Owned' and item['price'] is not None]

        if used_prices:
            used_mean_price, used_lower_bound, used_upper_bound, used_certainty = _calculate_price_bounds(used_prices)
        else:
            return Product({}, data_description="price", data_type="price"), False

        result = {
            'price': used_mean_price,
            'min_range': used_lower_bound,
            'max_range': used_upper_bound,
            'certainty': used_certainty
        }
        return Product(result, data_description="estimated-price", data_type="dict[str,str]"), True  # type: ignore


def _calculate_price_bounds(prices_raw: list[float]) -> tuple[float, float, float, float]:
    prices = np.array(prices_raw)
    n = len(prices)
    median_price = np.median(prices)

    # Calculate weights
    position_weights = np.linspace(1, 0.5, n)  # Decreasing weights for later results
    deviation_weights = np.exp(-((prices - median_price) / median_price)**2)  # Less weight for extreme prices

    weights = position_weights * deviation_weights

    # Weighted statistics
    weighted_mean_price = np.average(prices, weights=weights)
    weighted_std_price = np.sqrt(np.average((prices - weighted_mean_price)**2, weights=weights))

    # Using IQR for more robust bounds
    q25, q75 = np.percentile(prices, [25, 75])
    iqr = q75 - q25
    lower_bound = max(q25 - 1 * iqr, 0)
    upper_bound = q75 + 1.5 * iqr

    # Certainty based on the percentage of prices within one weighted standard deviation of the weighted mean
    within_one_std = np.sum((prices >= weighted_mean_price - weighted_std_price) & (prices <= weighted_mean_price + weighted_std_price))
    certainty = within_one_std / len(prices)

    return weighted_mean_price, lower_bound, upper_bound, certainty