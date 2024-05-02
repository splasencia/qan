const request = require('supertest');
const app = require('../server'); // Asegúrate de que tu servidor exporta la aplicación de Express

describe('GET /links', () => {
    it('should return a list of links', async () => {
        const response = await request(app).get('/links');
        expect(response.statusCode).toBe(200);
        expect(response.body).toBeInstanceOf(Array);
    });
});
