const baseUrl = '/bothub/';

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
  url: 'https://ilhasoft.bothub.it',
  baseUrl,
  projectName: 'bothub',
  organizationName: 'Ilhasoft',
  headerLinks: [
    {doc: 'doc1', label: 'Docs'},
    {doc: 'doc4', label: 'API'},
    {page: 'help', label: 'Help'},
    {blog: true, label: 'Blog'},
  ],
  users,
  headerIcon: 'img/docusaurus.svg',
  footerIcon: 'img/docusaurus.svg',
  favicon: 'img/favicon.png',
  colors: {
    primaryColor: '#2E8555',
    secondaryColor: '#205C3B',
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
};

module.exports = siteConfig;
