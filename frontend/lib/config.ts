export default class Config {
  static get apiUrl(): string {
    return process.env.NEXT_PUBLIC_API_URL || 'http://localhost:3002';
  }
}
