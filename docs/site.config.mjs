export default {
  // required by remote-astro-theme
  theme: "mindovermachine-dev/mom-doc-theme@main",

  // Overrides the theme's astro.config.mjs settings (Starlight)
  title: "gh-tt",
  site: "https://devx-cafe.github.io",
  rootRedirect: null,
  defaultLocale: "root",
  locales: { root: { label: "English", lang: "en" } },
  astro: { base: "/gh-tt", server: { host: true } },
  social: [
    {
      icon: "github",
      label: "GitHub",
      href: "https://github.com/devx-cafe/gh-tt",
    },
  ],
  sidebar: [
    {
      label: "Guide",
      items: [{ autogenerate: { directory: "guide" } }],
    },
    {
      label: "Commands",
      items: [{ autogenerate: { directory: "commands" } }],
    },
    {
      label: "Development",
      items: [{ autogenerate: { directory: "development" } }],
    },
  ],
};
