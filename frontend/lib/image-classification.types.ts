type ClassificationDataType = {
  unknown: any;
  'model-producer': {
    model: string;
    producer: string;
  };
  'producer-url': {
    title: string;
    link: string;
  };
  'retail-price-details': {
    producer_url: string;
    price: number;
    original_name: string;
    description: string;
    material: string;
    specs: string;
  };
  'estimated-price': {
    price: number;
    certainty: string;
    min_range: number;
    max_range: number;
  };
  'second-hand-offers': {
    link: string;
    price: number;
    wear: string;
  }[];
};

export type ClassificationProductDescription = keyof ClassificationDataType;

export type ClassificationProduct<
  T extends ClassificationProductDescription = ClassificationProductDescription
> = {
  data: ClassificationDataType[T];
  data_description: T;
  data_type: string;
};
