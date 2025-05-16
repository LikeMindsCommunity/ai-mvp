import { HawcxInitializer } from "https://websdkcdn.hawcx.com/hawcx-auth.esm.min.js";

const API_KEY = 'LmVKd2x5a0VPZ3lBUUFNQ19jRzRhdGlLd1BmVW5aSUhGb2tXTmFJeHQtdmVhZE03ekVWdmx4ZVVvN21La2xldno4Y29EbHp6R2VnMVRLZHVZMTBOY0JNM3pmM1YxaVN2c0VLZnVYZnAtVWxsMWVJYUZka2R6ZGdNZjV3SWZHUzBTYWVBb2syeGFxYUFKclE4eVNvMHlOSmE5TnBTU0IwS054dDRVaEdTTTlpalphdkg5QVFtRk1Xdy5hQ1hYVGcuTjBvcnRiNGNlRUdQT2J2SFpJTjNwRTJEaHZCQWJ5NmpURzBlVDdmQkNsS1U5LXdSMkduN1RTR1pGaEx5UXZyekd4Umx3SFFEdkNGUS0tVFdRNERGQmc='; // TODO: Replace with your Hawcx API key
let auth;

async function initAuth() {
  auth = await HawcxInitializer.init(API_KEY);
}

function render() {
  document.getElementById('root').innerHTML = `
    <div class="card p-4">
      <h2 class="mb-4 text-center">Hawcx Auth Demo</h2>
      <ul class="nav nav-tabs mb-3" id="authTabs">
        <li class="nav-item">
          <a class="nav-link active" id="signInTab" href="#">Sign In</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" id="registerTab" href="#">Register</a>
        </li>
      </ul>
      <div id="formContainer"></div>
      <div id="message" class="mt-3"></div>
    </div>
  `;
  showSignInForm();
  document.getElementById('signInTab').onclick = (e) => { e.preventDefault(); switchTab('signIn'); };
  document.getElementById('registerTab').onclick = (e) => { e.preventDefault(); switchTab('register'); };
}

function switchTab(tab) {
  document.getElementById('signInTab').classList.toggle('active', tab === 'signIn');
  document.getElementById('registerTab').classList.toggle('active', tab === 'register');
  if (tab === 'signIn') {
    showSignInForm();
  } else {
    showRegisterForm();
  }
}

function showSignInForm() {
  document.getElementById('formContainer').innerHTML = `
    <form id="signInForm">
      <div class="mb-3">
        <label for="signInEmail" class="form-label">Email address</label>
        <input type="email" class="form-control" id="signInEmail" required />
      </div>
      <button type="submit" class="btn btn-primary w-100">Sign In</button>
    </form>
  `;
  document.getElementById('signInForm').onsubmit = handleSignIn;
}

function showRegisterForm() {
  document.getElementById('formContainer').innerHTML = `
    <form id="registerForm">
      <div class="mb-3">
        <label for="registerEmail" class="form-label">Email address</label>
        <input type="email" class="form-control" id="registerEmail" required />
      </div>
      <div class="mb-3">
        <label for="registerOtp" class="form-label">OTP (after requesting)</label>
        <input type="text" class="form-control" id="registerOtp" />
      </div>
      <button type="submit" class="btn btn-success w-100">Register</button>
    </form>
  `;
  document.getElementById('registerForm').onsubmit = handleRegister;
}

async function handleSignIn(e) {
  e.preventDefault();
  const email = document.getElementById('signInEmail').value;
  setMessage('Signing in...', 'info');
  try {
    const response = await auth.signIn(email);
    if (response.success) {
      const { access_token, refresh_token } = response.data;
      sessionStorage.setItem('access_token', access_token);
      setMessage('Login successful!', 'success');
    } else {
      setMessage(response.error || 'Sign in failed', 'danger');
    }
  } catch (err) {
    setMessage('Sign in error: ' + err.message, 'danger');
  }
}

let registrationSessionId = null;

async function handleRegister(e) {
  e.preventDefault();
  const email = document.getElementById('registerEmail').value;
  const otp = document.getElementById('registerOtp').value;
  if (!registrationSessionId && !otp) {
    setMessage('Requesting OTP...', 'info');
    try {
      const response = await auth.signUp(email);
      if (response.success) {
        registrationSessionId = response.data.sessionId;
        setMessage('OTP sent to your email. Enter it below to complete registration.', 'success');
      } else {
        setMessage(response.error || 'Registration failed', 'danger');
      }
    } catch (err) {
      setMessage('Registration error: ' + err.message, 'danger');
    }
  } else if (registrationSessionId && otp) {
    setMessage('Verifying OTP...', 'info');
    try {
      const verify = await auth.verifyOTP(otp);
      if (verify.success) {
        setMessage('User registration completed successfully.', 'success');
        registrationSessionId = null;
        document.getElementById('registerForm').reset();
      } else {
        setMessage(verify.error || 'OTP verification failed', 'danger');
      }
    } catch (err) {
      setMessage('OTP verification error: ' + err.message, 'danger');
    }
  } else {
    setMessage('Please enter the OTP sent to your email.', 'warning');
  }
}

function setMessage(msg, type = 'info') {
  document.getElementById('message').innerHTML = `<div class="alert alert-${type}">${msg}</div>`;
}

initAuth().then(render); 