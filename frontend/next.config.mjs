/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
  rewrites: async () => {
    return [
      {
        source: '/api/:path*',
        destination: 'http://192.168.178.41:3002/:path*',
      },
    ];
  },
};

export default nextConfig;
