import {
  ClassificationProduct,
  ClassificationProductDescription,
} from '@/lib/image-classification.types';

type CardDataKeyMap = Record<string, React.ReactNode>;
type CardDataValueMap = Record<string, (value: string) => React.ReactNode>;

const linkMapper = (value: string) => (
  <a
    href={value}
    target="_blank"
    rel="noopener noreferrer"
    className="underline"
  >
    {value}
  </a>
);

const euroFormatter = (value: number | string) => {
  if (typeof value === 'string') {
    const parsedValue = parseFloat(value).toFixed(2);

    return `€${parsedValue}`;
  }

  return `€${value.toFixed(2)}`;
};

const percentageFormatter = (value: string | number) => {
  if (typeof value === 'string') {
    const parsedValue = (parseFloat(value) * 100).toFixed(1);

    return `${parsedValue}%`;
  }

  return `${(value * 100).toFixed(1)}%`;
};

export function ClassificationCardContent<
  T extends ClassificationProductDescription
>({
  data,
  keyMap = {},
  valueMap = {},
}: {
  data: ClassificationProduct<T>['data'];
  keyMap?: CardDataKeyMap;
  valueMap?: CardDataValueMap;
}) {
  const entries: [string, string][] = Object.entries(data);

  const getKey = (key: string) => keyMap[key] || key.toString();
  const getValue = (key: string, value: string) =>
    valueMap[key]?.(value as string) || value;

  return (
    <ul>
      {entries.map(([key, value]) => (
        <div
          key={key as string}
          className="flex flex-row justify-between text-sm mt-4 gap-4"
        >
          <li className="font-bold">{getKey(key)}</li>
          <li className="text-end text-muted-foreground text-ellipsis overflow-hidden">
            {getValue(key, value)}
          </li>
        </div>
      ))}
    </ul>
  );
}

export function ClassificationCardProducerUrl({
  data,
}: {
  data: ClassificationProduct<'producer-url'>['data'];
}) {
  const keyMap = {
    title: 'Title',
    link: 'Link',
  };

  const valueMap = {
    link: linkMapper,
  };

  return (
    <ClassificationCardContent
      data={data}
      keyMap={keyMap}
      valueMap={valueMap}
    />
  );
}

export function ClassificationCardEstimatedPrice({
  data,
}: {
  data: ClassificationProduct<'estimated-price'>['data'];
}) {
  const keyMap = {
    price: 'Price',
    certainty: 'Certainty',
    min_range: 'Min Range',
    max_range: 'Max Range',
  };

  const valueMap = {
    price: euroFormatter,
    min_range: euroFormatter,
    max_range: euroFormatter,
    certainty: percentageFormatter,
  };

  return (
    <ClassificationCardContent
      data={data}
      keyMap={keyMap}
      valueMap={valueMap}
    />
  );
}

export function ClassificationCardSecondHandOffers({
  data,
}: {
  data: ClassificationProduct<'second-hand-offers'>['data'];
}) {
  const keyMap = {
    link: 'Link',
    price: 'Price',
    wear: 'Wear',
  };

  const valueMap = {
    link: linkMapper,
    price: euroFormatter,
  };

  return (
    <>
      {data.map((offer, index) => (
        <>
          <ClassificationCardContent
            key={index}
            data={offer}
            keyMap={keyMap}
            valueMap={valueMap}
          />

          {index < data.length - 1 && <hr className="my-4" />}
        </>
      ))}
    </>
  );
}

export function ClassificationCardRetailPrice({
  data,
}: {
  data: ClassificationProduct<'retail-price-details'>['data'];
}) {
  const keyMap = {
    producer_url: 'Producer URL',
    price: 'Retail Price',
    original_name: 'Original Name',
    description: 'Description',
    material: 'Material',
    color: 'Color',
    specs: 'Specs',
  };

  const valueMap = {
    producer_url: linkMapper,
  };

  return (
    <ClassificationCardContent
      data={data}
      keyMap={keyMap}
      valueMap={valueMap}
    />
  );
}

export function ClassificationCardModelProducer({
  data,
}: {
  data: ClassificationProduct<'model-producer'>['data'];
}) {
  const keyMap = {
    model: 'Model',
    producer: 'Producer',
  };

  return <ClassificationCardContent data={data} keyMap={keyMap} />;
}
