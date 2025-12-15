/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  // Configure path aliases
  webpack: (config) => {
    config.resolve.alias = {
      ...config.resolve.alias,
      '@': __dirname,
    };
    return config;
  },
}

module.exports = nextConfig
