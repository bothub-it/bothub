const React = require('react');

class Footer extends React.Component {
  docUrl(doc, language) {
    const baseUrl = this.props.config.baseUrl;
    return `${baseUrl}docs/${language ? `${language}/` : ''}${doc}`;
  }

  pageUrl(doc, language) {
    const baseUrl = this.props.config.baseUrl;
    return baseUrl + (language ? `${language}/` : '') + doc;
  }

  render() {
    return (
      <footer className="nav-footer" id="footer">
        <section className="sitemap">
          <a href={this.props.config.baseUrl} className="nav-home">
            {this.props.config.footerIcon && (
              <img
                src={this.props.config.baseUrl + this.props.config.footerIcon}
                alt={this.props.config.title}
                width="66"
              />
            )}
          </a>
          <div>
            <h5>Docs</h5>
            <a href={this.docUrl('bothub.html', this.props.language)}>
              Bothub
            </a>
            <a href={this.docUrl('parse.html', this.props.language)}>
              NLU Parse
            </a>
            <a href={this.docUrl('api.html', this.props.language)}>
              API
            </a>
          </div>
          <div>
            <h5>Community</h5>
            <a href={this.pageUrl('users.html', this.props.language)}>
              User Showcase
            </a>
            <a
              href="https://www.twitter.com"
              target="_blank">
              Twitter
            </a>
            <a
              href="https://www.facebook.com/bothub.it"
              target="_blank">
              Facebook
            </a>
          </div>
          <div>
            <h5>More</h5>
            <a href={`${this.props.config.baseUrl}blog`}>Blog</a>
            <a href={`https://github.com/${this.props.config.repoUrl}`}>GitHub</a>
            <a
              className="github-button"
              href={`https://github.com/${this.props.config.repoUrl}`}
              data-icon="octicon-star"
              data-show-count="true"
              aria-label={`Star ${this.props.config.repoUrl} on GitHub`}>
              Star
            </a>
          </div>
        </section>
        <section className="copyright">{this.props.config.copyright}</section>
      </footer>
    );
  }
}

module.exports = Footer;
