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
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'a.dropoverapp.com',
        port: '',
        pathname: '**',
      },
    ],
  },
};

export default nextConfig;
