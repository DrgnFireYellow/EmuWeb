import clsx from 'clsx';
import Heading from '@theme/Heading';
import styles from './styles.module.css';

const FeatureList = [
  {
    title: 'Get Started in 10 Minutes',
    Svg: require('@site/static/img/promo-setup.svg').default,
    description: (
      <>
        EmuWeb is simple to setup and works almost out of the box.
      </>
    ),
  },
  {
    title: 'Play on Any Device',
    Svg: require('@site/static/img/promo-multiplatform.svg').default,
    description: (
      <>
        Since EmuWeb is a webapp, you can play your games on any device. Maybe even your toaster!
      </>
    ),
  },
  {
    title: 'Lightning Fast',
    Svg: require('@site/static/img/promo-performance.svg').default,
    description: (
      <>
        Most games load in a matter of seconds.
      </>
    ),
  },
];

function Feature({Svg, title, description}) {
  return (
    <div className={clsx('col col--4')}>
      <div className="text--center">
        <Svg className={styles.featureSvg} role="img" />
      </div>
      <div className="text--center padding-horiz--md">
        <Heading as="h3">{title}</Heading>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures() {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}
