import http from 'k6/http';
import { sleep } from 'k6';

export const options = {
  stages: [
    { duration: '30s', target: 20 }, // ramp up to 20 users over 30s
    { duration: '1m', target: 20 },   // stay at 20 users for 1 minute
    { duration: '10s', target: 0 },  // ramp down to 0 users
  ],
};

export default function () {
  // Hit the success endpoint
  http.get('http://localhost:8000/');
  sleep(1);

  // Occasionally hit the error endpoint
  if (Math.random() > 0.8) {
    http.get('http://localhost:8000/error');
  }
}
