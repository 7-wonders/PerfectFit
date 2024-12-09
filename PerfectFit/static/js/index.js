const instance = axios.create({
    baseURL: 'http://127.0.0.1:5000',
    timeout: 30000,
    headers: {
      'Content-Type': 'application/json'
    },
    withCredentials: true,
    responseType: 'json',
    responseEncoding: 'utf8',
});

async function getUser() {
  try {
    const response = await instance.get('/user/1');
    console.log(response);
  } catch (error) {
    console.error(error);
  }
}