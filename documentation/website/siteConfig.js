const baseUrl = '/';

const users = [
  {
    caption: 'Push',
    image: `${baseUrl}img/push.al.png`,
    infoLink: 'https://push.al',
    pinned: true,
  },
];

const siteConfig = {
  title: 'Bothub',
  tagline: 'An open platform for predicting, training and sharing NLP datasets in multiple languages.',
  url: 'https://docs.bothub.it',
  baseUrl,
  projectName: 'bothub',
  organizationName: 'Ilhasoft',
  headerLinks: [
    {doc: 'bothub', label: 'Docs'},
    {doc: 'api', label: 'API'},
    {doc: 'nlu', label: 'NLU'},
    {page: 'help', label: 'Help'},
    {blog: true, label: 'Blog'},
  ],
  users,
  headerIcon: 'img/botinho.svg',
  footerIcon: 'img/botinho.svg',
  favicon: 'img/favicon.png',
  colors: {
    primaryColor: '#00E676',
    secondaryColor: '#00C853',
  },
  copyright: `Copyright © ${new Date().getFullYear()} Bothub`,
  highlight: {
    theme: 'default',
  },
  scripts: ['https://buttons.github.io/buttons.js'],
  onPageNav: 'separate',
  cleanUrl: true,
  ogImage: 'img/docusaurus.png',
  twitterImage: 'img/docusaurus.png',
  repoUrl: 'Ilhasoft/bothub',
};

module.exports = siteConfig;
