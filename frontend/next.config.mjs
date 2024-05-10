/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
  rewrites: async () => {
    return [
      {
        source: '/api/:path*',
        destination: 'http://localhost:3002/:path*',
      },
    ];
  },
};

export default nextConfig;
