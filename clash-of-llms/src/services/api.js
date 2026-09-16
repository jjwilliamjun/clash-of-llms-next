import axios from 'axios';

/**
 * Shared HTTP client for the Flask backend.
 *
 * The backend is a separate process on its own port, so the frontend has to be told
 * where it is rather than assuming. `VUE_APP_API_BASE_URL` is inlined by vue-cli at
 * build time (see `.env.example`); the default matches a Flask server started with
 * `flask run` on this machine.
 *
 * Note the host spelling matters. To a browser, `http://localhost:5000` and
 * `http://127.0.0.1:5000` are different origins and are matched separately by CORS,
 * so the backend's allowed-origin list has to name whichever one is used here.
 *
 * Requests for the frontend's own static files — anything under `/documents/` — must
 * NOT go through this client. Those are served by the dev server alongside the app,
 * not by Flask.
 */
const baseURL = process.env.VUE_APP_API_BASE_URL || 'http://127.0.0.1:5000';

export default axios.create({ baseURL });
