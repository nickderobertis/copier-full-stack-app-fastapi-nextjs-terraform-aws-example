module.exports = {
  stories: [
    "../components/**/__stories__/*.stories.@(js|jsx|ts|tsx|mdx)",
    "../pages/**/__stories__/*.stories.@(js|jsx|ts|tsx|mdx)",
  ],
  addons: [
    "@storybook/addon-links",
    "@storybook/addon-essentials",
    "@storybook/addon-interactions",
  ],
  framework: "@storybook/react",
  core: {
    builder: "@storybook/builder-webpack5",
  },
};
