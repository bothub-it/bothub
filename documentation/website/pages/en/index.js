const React = require('react');

const CompLibrary = require('../../core/CompLibrary.js');
const translate = require('../../server/translate.js').translate;

const MarkdownBlock = CompLibrary.MarkdownBlock;
const Container = CompLibrary.Container;
const GridBlock = CompLibrary.GridBlock;

const siteConfig = require(`${process.cwd()}/siteConfig.js`);

function imgUrl(img) {
  return `${siteConfig.baseUrl}img/${img}`;
}

function docUrl(doc, language) {
  return `${siteConfig.baseUrl}docs/${language ? `${language}/` : ''}${doc}`;
}

function pageUrl(page, language) {
  return siteConfig.baseUrl + (language ? `${language}/` : '') + page;
}

class Button extends React.Component {
  render() {
    return (
      <div className="pluginWrapper buttonWrapper">
        <a className="button" href={this.props.href} target={this.props.target}>
          {this.props.children}
        </a>
      </div>
    );
  }
}

Button.defaultProps = {
  target: '_self',
};

const SplashContainer = props => (
  <div className="homeContainer">
    <div className="homeSplashFade">
      <div className="wrapper homeWrapper">{props.children}</div>
    </div>
  </div>
);

const ProjectTitle = () => (
  <h2 className="projectTitle">
    {siteConfig.title}
    <small>{siteConfig.tagline}</small>
  </h2>
);

const PromoSection = props => (
  <div className="section promoSection">
    <div className="promoRow">
      <div className="pluginRowBlock">{props.children}</div>
    </div>
  </div>
);

class HomeSplash extends React.Component {
  render() {
    const language = this.props.language || '';
    return (
      <SplashContainer>
        <div className="inner">
          <ProjectTitle />
          <PromoSection>
            <Button href="https://bothub.it/" target="_blank"><translate>Create your bots</translate></Button>
            <Button href={docUrl('bothub.html', language)}><translate>About Bothub</translate></Button>
            <Button href={docUrl('api.html', language)}><translate>Bothub API</translate></Button>
            <Button href={docUrl('nlu.html', language)}><translate>NLU Docs</translate></Button>
          </PromoSection>
        </div>
      </SplashContainer>
    );
  }
}

const Block = props => (
  <Container
    padding={['bottom', 'top']}
    id={props.id}
    background={props.background}>
    <GridBlock align="center" contents={props.children} layout={props.layout} />
  </Container>
);

const Features = () => (
  <Block layout="fourColumn">
    {[
      {
        content: 'Support languages and dialects',
        image: imgUrl('icon/earth.png'),
        imageAlign: 'top',
        title: 'Multi language support',
      },
      {
        content: 'Without cost or payment',
        image: imgUrl('icon/thumb-up.png'),
        imageAlign: 'top',
        title: 'Free',
      },
      {
        content: 'Check our code in Github',
        image: imgUrl('icon/github-circle.png'),
        imageAlign: 'top',
        title: 'Open Source',
      },
    ]}
  </Block>
);

const Description = () => (
  <Block background="light">
    {[
      {
        content: 'This project is powered by [Ilhasoft](http://www.ilhasoft.com.br/en/), a Brazilian enterprise.',
        title: 'Powered by Ilhasoft',
      },
    ]}
  </Block>
);

const Showcase = props => {
  if ((siteConfig.users || []).length === 0) {
    return null;
  }

  const showcase = siteConfig.users.filter(user => user.pinned).map(user => (
    <a href={user.infoLink} key={user.infoLink}>
      <img src={user.image} alt={user.caption} title={user.caption} />
    </a>
  ));

  return (
    <div className="productShowcaseSection paddingBottom">
      <h2><translate>Who is Using This?</translate></h2>
      <p><translate>This project is used by all these people</translate></p>
      <div className="logos">{showcase}</div>
      <div className="more-users">
        <a className="button" href={pageUrl('users.html', props.language)}>
          <translate>More Users</translate>
        </a>
      </div>
    </div>
  );
};

class Index extends React.Component {
  render() {
    const language = this.props.language || '';

    return (
      <div>
        <HomeSplash language={language} />
        <div className="mainContainer">
          <Features />
          <Description />
          <Showcase language={language} />
        </div>
      </div>
    );
  }
}

module.exports = Index;
