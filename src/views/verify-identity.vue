<template>
  <div class="verify-identity-bg">
    <div class="verify-identity-main">
      <div class="verify-identity-card">
        <div class="verify-identity-header">
          <div class="verify-icon">
            <i class="fas fa-user-shield"></i>
          </div>
          <h2 class="verify-identity-title">Verify Identity</h2>
          <p class="verify-identity-subtitle">Please confirm your name to continue</p>
        </div>
        
        <form @submit.prevent="handleSubmit" class="verify-identity-form">
          <div class="form-group">
            <label for="full-name">Full Name</label>
            <div class="input-container">
              <input 
                type="text" 
                id="full-name"
                v-model="fullName" 
                placeholder="Enter your full name"
                required
              />
            </div>
          </div>
          
          <div class="form-group">
            <label for="confirm-email">Confirm Email</label>
            <div class="input-container">
              <input 
                type="email" 
                id="confirm-email"
                v-model="email" 
                placeholder="Confirm your email address"
                required
                :readonly="emailFromParams"
              />
            </div>
          </div>
          
          <button 
            type="submit" 
            class="send-reset-btn"
            :disabled="isSubmitting"
          >
            <span v-if="isSubmitting" class="spinner"></span>
            {{ isSubmitting ? 'Verifying...' : 'Send Reset Link' }}
          </button>
        </form>
        
        <div v-if="errorMessage" class="error-message">
          {{ errorMessage }}
        </div>
        
        <div class="bottom-link">
          Go back to <router-link to="/login">Sign in</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '@/utils/axios';

export default {
  name: 'VerifyIdentityPage',
  data() {
    return {
      email: '',
      fullName: '',
      isSubmitting: false,
      errorMessage: '',
      emailFromParams: false
    };
  },
  created() {
    // Check if email was passed from the forgot password page
    const routeEmail = this.$route.params.email;
    
    if (routeEmail) {
      this.email = routeEmail;
      this.emailFromParams = true;
    }
  },
  methods: {
    async handleSubmit() {
      this.isSubmitting = true;
      this.errorMessage = '';

      try {
        // For development/testing, we'll immediately redirect to reset password
        // In production, this would contact your API
        
        // Normally we would verify user identity with API:
        // const response = await api.post('/verify-identity', { 
        //   email: this.email,
        //   fullName: this.fullName
        // });
        
        // For now, use a mock token and redirect
        const mockToken = 'reset-token-' + Math.random().toString(36).substring(2);
        
        // Redirect to reset password with token
        this.$router.push({
          name: 'reset-password',
          query: { 
            token: mockToken 
          }
        });
      } catch (error) {
        console.error('Error verifying identity:', error);
        this.errorMessage = error.response?.data?.message || 'An error occurred. Please try again later.';
      } finally {
        this.isSubmitting = false;
      }
    }
  }
};
</script>

<style scoped>
.verify-identity-bg {
  height: 100vh;
  background: #f4f6fa;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}

.verify-identity-main {
  height: 100vh;
  width: 100vw;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.verify-identity-card {
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 8px 30px rgba(0,0,0,0.08);
  width: 100%;
  max-width: 450px;
  padding: 40px 30px;
  text-align: center;
}

.verify-identity-header {
  margin-bottom: 30px;
}

.verify-icon {
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

.verify-icon i {
  font-size: 36px;
  color: #f7871f;
}

.verify-identity-title {
  color: #222;
  font-size: 24px;
  font-weight: 700;
  margin-bottom: 10px;
}

.verify-identity-subtitle {
  color: #666;
  font-size: 16px;
}

.verify-identity-form {
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

.input-container input[readonly] {
  background-color: #f8f8f8;
  color: #777;
}

.send-reset-btn {
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

.send-reset-btn:hover {
  background: #e67012;
}

.send-reset-btn:disabled {
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
  .verify-identity-card {
    padding: 30px 20px;
  }
  
  .verify-identity-title {
    font-size: 22px;
  }
  
  .verify-identity-subtitle {
    font-size: 14px;
  }
}
</style>
