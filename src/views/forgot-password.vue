<template>
  <div class="forgot-password-bg">
    <div class="forgot-password-main">
      <div class="forgot-password-card">
        <div class="forgot-password-header">
          <!-- Replace image with Font Awesome icon -->
          <div class="forget-icon">
            <i class="fas fa-envelope"></i>
          </div>
          <h2 class="forgot-password-title">Forgot Password</h2>
          <p class="forgot-password-subtitle">Enter your email to receive a reset link</p>
        </div>
        
        <form v-if="!emailSent" @submit.prevent="handleSubmit" class="forgot-password-form">
          <div class="form-group">
            <label for="email-address">Email address</label>
            <div class="input-container">
              <input 
                type="email" 
                id="email-address"
                v-model="email" 
                placeholder="Email address"
                required
              />
            </div>
          </div>
          
          <button 
            type="submit" 
            class="confirm-btn"
            :disabled="isSubmitting"
          >
            <span v-if="isSubmitting" class="spinner"></span>
            {{ isSubmitting ? 'Processing...' : 'Reset Password' }}
          </button>
        </form>

        <div v-if="emailSent" class="success-message-container">
          <div class="success-icon">
            <i class="fas fa-envelope-open-text"></i>
          </div>
          <h3 class="success-title">Check Your Email</h3>
          <p class="success-text">
            We've sent a password reset link to:
            <strong>{{ email }}</strong>
          </p>
          <p class="success-instruction">
            Click the link in the email to reset your password. The link will expire in 24 hours.
            If you don't see the email, check your spam folder.
          </p>
          <div class="additional-options">
            <button @click="handleSubmit" class="resend-btn">
              <i class="fas fa-redo-alt"></i> Resend Email
            </button>
          </div>
        </div>
        
        <div v-if="errorMessage" class="error-message">
          {{ errorMessage }}
        </div>
        
        <div class="bottom-link">
          Remembered your password? <router-link to="/login">Sign in</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '@/utils/axios';

export default {
  name: 'ForgotPasswordPage',
  data() {
    return {
      email: '',
      isSubmitting: false,
      errorMessage: '',
      emailSent: false
    };
  },
  methods: {
    async handleSubmit() {
      if (this.isSubmitting) return;
      
      this.isSubmitting = true;
      this.errorMessage = '';

      try {
        // Call the backend API to check email and send reset link
        const response = await api.post('/check-email', { 
          email: this.email 
        });

        if (response.data.success) {
          // Show success message
          this.emailSent = true;
        } else {
          this.errorMessage = response.data.message || 'Email not found in our system.';
        }
      } catch (error) {
        console.error('Error checking email:', error);
        this.errorMessage = error.response?.data?.message || 'An error occurred. Please try again later.';
        this.emailSent = false;
      } finally {
        this.isSubmitting = false;
      }
    }
  }
};
</script>

<style scoped>
.forgot-password-bg {
  height: 100vh;
  background: #f4f6fa;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}

.forgot-password-main {
  height: 100vh;
  width: 100vw;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.forgot-password-card {
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 8px 30px rgba(0,0,0,0.08);
  width: 100%;
  max-width: 450px;
  padding: 40px 30px;
  text-align: center;
}

.forgot-password-header {
  margin-bottom: 30px;
}

.forget-icon {
  width: 80px;
  height: 80px;
  margin-bottom: 20px;
  background-color: #fff5eb;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 20px auto;
}

.forget-icon i {
  font-size: 36px;
  color: #f7871f;
}

.forgot-password-title {
  color: #222;
  font-size: 24px;
  font-weight: 700;
  margin-bottom: 10px;
}

.forgot-password-subtitle {
  color: #666;
  font-size: 16px;
}

.forgot-password-form {
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 20px;
  text-align: left;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  color: #444;
  font-size: 14px;
  font-weight: 500;
}

.input-container {
  position: relative;
}

.input-container input {
  width: 100%;
  padding: 14px;
  border: 1.5px solid #e0e0e0;
  border-radius: 8px;
  font-size: 16px;
  transition: border-color 0.3s;
}

.input-container input:focus {
  border-color: #f7871f;
  outline: none;
}

.confirm-btn {
  width: 100%;
  padding: 14px;
  background: #f7871f;
  color: #fff;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.3s;
  position: relative;
}

.confirm-btn:hover {
  background: #e67012;
}

.confirm-btn:disabled {
  background: #ffa55e;
  cursor: not-allowed;
}

.spinner {
  display: inline-block;
  width: 18px;
  height: 18px;
  border: 3px solid rgba(255,255,255,0.3);
  border-radius: 50%;
  border-top-color: #fff;
  animation: spin 1s ease-in-out infinite;
  position: absolute;
  right: 20px;
  top: 50%;
  transform: translateY(-50%);
}

@keyframes spin {
  to { transform: translateY(-50%) rotate(360deg); }
}

.success-message-container {
  padding: 15px;
  text-align: center;
}

.success-icon {
  width: 80px;
  height: 80px;
  margin: 0 auto 20px auto;
  background-color: #f0f9f0;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.success-icon i {
  font-size: 36px;
  color: #28a745;
}

.success-title {
  color: #28a745;
  font-size: 20px;
  margin-bottom: 15px;
  font-weight: 700;
}

.success-text {
  margin-bottom: 10px;
  color: #444;
}

.success-instruction {
  color: #666;
  font-size: 14px;
  margin-bottom: 25px;
  line-height: 1.5;
}

.additional-options {
  margin-top: 20px;
}

.resend-btn {
  background: none;
  border: none;
  color: #f7871f;
  font-weight: 600;
  cursor: pointer;
  padding: 10px 15px;
  border-radius: 5px;
  transition: all 0.2s;
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.resend-btn:hover {
  background-color: #fff5eb;
  text-decoration: underline;
}

.error-message {
  color: #e74c3c;
  margin: 15px 0;
  font-size: 14px;
}

.bottom-link {
  color: #666;
  font-size: 14px;
  margin-top: 20px;
}

.bottom-link a {
  color: #f7871f;
  text-decoration: none;
  font-weight: 600;
}

.bottom-link a:hover {
  text-decoration: underline;
}

@media (max-width: 480px) {
  .forgot-password-card {
    padding: 30px 20px;
  }
  
  .forgot-password-title {
    font-size: 22px;
  }
  
  .forgot-password-subtitle {
    font-size: 14px;
  }
}
</style>
