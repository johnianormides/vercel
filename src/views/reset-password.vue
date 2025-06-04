<template>
  <div class="reset-password-bg">
    <div class="reset-password-main">
      <div class="reset-password-card">
        <div v-if="invalidToken" class="invalid-token-container">
          <div class="error-icon">
            <i class="fas fa-exclamation-triangle"></i>
          </div>
          <h3 class="error-title">Invalid or Expired Link</h3>
          <p class="error-text">
            The password reset link you used is either invalid or has expired.
          </p>
          <router-link to="/forgot-password" class="request-new-link">
            Request a new password reset link
          </router-link>
        </div>

        <div v-else>
          <div class="reset-password-header">
            <div class="reset-icon">
              <i class="fas fa-lock"></i>
            </div>
            <h2 class="reset-password-title">Reset Password</h2>
            <p class="reset-password-subtitle">Enter your new password below</p>
          </div>
          
          <form @submit.prevent="handleSubmit" class="reset-password-form">
            <div class="form-group">
              <label for="new-password">New Password</label>
              <div class="input-container password-container">
                <input 
                  :type="showPassword ? 'text' : 'password'" 
                  id="new-password"
                  v-model="newPassword" 
                  placeholder="New Password"
                  required
                  @input="validatePassword"
                />
                <span class="password-toggle" @click="showPassword = !showPassword">
                  <i v-if="showPassword" class="fas fa-eye"></i>
                  <i v-else class="fas fa-eye-slash"></i>
                </span>
              </div>
              <div class="password-rules" v-show="showPasswordValidation">
                <div :class="{ valid: passwordValidation.length }">• At least 8 characters</div>
                <div :class="{ valid: passwordValidation.upper }">• One uppercase letter</div>
                <div :class="{ valid: passwordValidation.number }">• One number</div>
                <div :class="{ valid: passwordValidation.special }">• One special character</div>
              </div>
            </div>
            
            <div class="form-group">
              <label for="confirm-password">Confirm Password</label>
              <div class="input-container password-container">
                <input 
                  :type="showPassword ? 'text' : 'password'" 
                  id="confirm-password"
                  v-model="confirmPassword" 
                  placeholder="Confirm Password"
                  required
                  :class="{ 'password-mismatch': passwordMismatch }"
                />
                <span class="password-toggle" @click="showPassword = !showPassword">
                  <i v-if="showPassword" class="fas fa-eye"></i>
                  <i v-else class="fas fa-eye-slash"></i>
                </span>
              </div>
              <div v-if="passwordMismatch" class="mismatch-error">
                Passwords do not match
              </div>
            </div>
            
            <button 
              type="submit" 
              class="reset-btn"
              :disabled="!allValidationsPassed || isSubmitting"
            >
              <span v-if="isSubmitting" class="spinner"></span>
              {{ isSubmitting ? 'Processing...' : 'Reset Password' }}
            </button>
          </form>
          
          <div v-if="errorMessage" class="error-message">
            {{ errorMessage }}
          </div>
          
          <div v-if="successMessage" class="success-message">
            {{ successMessage }}
          </div>
        </div>
        
        <div class="bottom-link">
          Remember your password? <router-link to="/login">Sign in</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '@/utils/axios';

export default {
  name: 'ResetPasswordPage',
  data() {
    return {
      token: '',
      newPassword: '',
      confirmPassword: '',
      showPassword: false,
      showPasswordValidation: false,
      passwordValidation: {
        length: false,
        upper: false,
        number: false,
        special: false
      },
      isSubmitting: false,
      errorMessage: '',
      successMessage: '',
      invalidToken: false
    };
  },
  created() {
    // Get token from URL query parameters
    this.token = this.$route.query.token;
    
    if (!this.token) {
      this.invalidToken = true;
      return;
    }
    
    // Verify token validity
    this.verifyToken();
  },
  computed: {
    passwordMismatch() {
      return this.confirmPassword && this.newPassword !== this.confirmPassword;
    },
    allValidationsPassed() {
      return (
        this.passwordValidation.length &&
        this.passwordValidation.upper &&
        this.passwordValidation.number &&
        this.passwordValidation.special &&
        this.newPassword === this.confirmPassword &&
        this.newPassword.length > 0
      );
    }
  },
  methods: {
    async verifyToken() {
      try {
        const response = await api.post('/verify-reset-token', { token: this.token });
        
        if (!response.data.success) {
          this.invalidToken = true;
        }
      } catch (error) {
        console.error('Error verifying token:', error);
        this.invalidToken = true;
      }
    },
    validatePassword() {
      const password = this.newPassword;
      this.passwordValidation.length = password.length >= 8;
      this.passwordValidation.upper = /[A-Z]/.test(password);
      this.passwordValidation.number = /[0-9]/.test(password);
      this.passwordValidation.special = /[!@#$%^&*(),.?":{}|<>]/.test(password);
      this.showPasswordValidation = true;
    },
    async handleSubmit() {
      if (!this.allValidationsPassed) {
        return;
      }

      this.isSubmitting = true;
      this.errorMessage = '';
      this.successMessage = '';

      try {
        const response = await api.post('/reset-password', { 
          token: this.token,
          password: this.newPassword
        });

        if (response.data.success) {
          this.successMessage = 'Password reset successfully! Redirecting to login...';
          
          // Redirect to login after a short delay
          setTimeout(() => {
            this.$router.push('/login');
          }, 2000);
        } else {
          this.errorMessage = response.data.message || 'Password reset failed.';
        }
      } catch (error) {
        console.error('Error resetting password:', error);
        this.errorMessage = error.response?.data?.message || 'An error occurred. Please try again later.';
      } finally {
        this.isSubmitting = false;
      }
    }
  }
};
</script>

<style scoped>
.reset-password-bg {
  height: 100vh;
  background: #f4f6fa;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}

.reset-password-main {
  height: 100vh;
  width: 100vw;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.reset-password-card {
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 8px 30px rgba(0,0,0,0.08);
  width: 100%;
  max-width: 450px;
  padding: 40px 30px;
  text-align: center;
}

.reset-password-header {
  margin-bottom: 30px;
}

.reset-icon {
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

.reset-icon i {
  font-size: 36px;
  color: #f7871f;
}

.reset-password-title {
  color: #222;
  font-size: 24px;
  font-weight: 700;
  margin-bottom: 10px;
}

.reset-password-subtitle {
  color: #666;
  font-size: 16px;
}

.reset-password-form {
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 20px;
  text-align: left;
  position: relative;
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

.password-container {
  display: flex;
  align-items: center;
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

.input-container input.password-mismatch {
  border-color: #e74c3c;
  background-color: #fff6f6;
}

.password-toggle {
  position: absolute;
  right: 14px;
  top: 50%;
  transform: translateY(-50%);
  cursor: pointer;
  color: #666;
}

.password-toggle:hover {
  color: #f7871f;
}

.password-rules {
  margin-top: 10px;
  font-size: 12px;
  background: #f9f9f9;
  padding: 10px;
  border-radius: 5px;
  color: #666;
}

.password-rules div {
  margin-bottom: 5px;
}

.password-rules .valid {
  color: #27ae60;
}

.mismatch-error {
  color: #e74c3c;
  font-size: 12px;
  margin-top: 5px;
}

.reset-btn {
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

.reset-btn:hover:not(:disabled) {
  background: #e67012;
}

.reset-btn:disabled {
  background: #e0e0e0;
  color: #999;
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

.error-message {
  color: #e74c3c;
  margin: 15px 0;
  font-size: 14px;
}

.success-message {
  color: #27ae60;
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

.invalid-token-container {
  text-align: center;
  padding: 20px 0;
}

.error-icon {
  width: 80px;
  height: 80px;
  margin: 0 auto 20px auto;
  background-color: #fff5f5;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.error-icon i {
  font-size: 36px;
  color: #e74c3c;
}

.error-title {
  color: #e74c3c;
  font-size: 20px;
  margin-bottom: 15px;
}

.error-text {
  color: #666;
  margin-bottom: 25px;
}

.request-new-link {
  display: inline-block;
  background: #f7871f;
  color: white;
  padding: 12px 20px;
  border-radius: 6px;
  text-decoration: none;
  font-weight: 600;
  transition: background 0.2s;
}

.request-new-link:hover {
  background: #e67012;
}

@media (max-width: 480px) {
  .reset-password-card {
    padding: 30px 20px;
  }
  
  .reset-password-title {
    font-size: 22px;
  }
  
  .reset-password-subtitle {
    font-size: 14px;
  }
}
</style>
