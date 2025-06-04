<template>
  <div class="confirm-email">
    <div class="container">
      <div class="confirm-card">
        <div v-if="loading" class="text-center">
          <i class="fas fa-spinner fa-spin fa-2x mb-3"></i>
          <h3>Verifying your email...</h3>
          <p>Please wait while we confirm your email address.</p>
        </div>
        
        <div v-if="success && !loading" class="text-center">
          <i class="fas fa-check-circle text-success fa-3x mb-3"></i>
          <h2>Email Verified!</h2>
          <p>Your email has been successfully verified.</p>
          <p>You can now log in to your account and start browsing pets for adoption.</p>
          <div class="mt-4">
            <router-link to="/login" class="btn btn-primary">Login to Your Account</router-link>
          </div>
        </div>
        
        <div v-if="error && !loading" class="text-center">
          <i class="fas fa-exclamation-circle text-danger fa-3x mb-3"></i>
          <h2>Verification Failed</h2>
          <p>{{ errorMessage }}</p>
          <div class="mt-4">
            <router-link to="/login" class="btn btn-outline-secondary me-2">Try to Login</router-link>
            <router-link to="/signup" class="btn btn-primary">Sign Up Again</router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'ConfirmEmail',
  data() {
    return {
      loading: true,
      success: false,
      error: false,
      errorMessage: '',
      token: '',
      type: ''
    };
  },
  created() {
    // Extract token and type from URL query parameters
    this.token = this.$route.query.token;
    this.type = this.$route.query.type;
    
    if (!this.token) {
      this.loading = false;
      this.error = true;
      this.errorMessage = 'Verification token is missing. Please check your email link.';
      return;
    }
    
    this.verifyEmail();
  },
  methods: {
    verifyEmail() {
      const apiUrl = process.env.VUE_APP_API_URL || 'http://localhost:5000';
      
      axios.post(`${apiUrl}/api/verify-email`, {
        token: this.token
        // Our custom verification doesn't need the type parameter
      })
      .then(response => {
        if (response.data.success) {
          this.loading = false;
          this.success = true;
          
          // Store authentication state in localStorage
          localStorage.setItem('email_verified', 'true');
        } else {
          this.loading = false;
          this.error = true;
          this.errorMessage = response.data.message || 'Failed to verify your email. Please try again.';
        }
      })
      .catch(error => {
        this.loading = false;
        this.error = true;
        this.errorMessage = error.response?.data?.message || 'An error occurred during verification. Please try again later.';
        console.error('Email verification error:', error);
      });
    }
  }
};
</script>

<style scoped>
.confirm-email {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 80vh;
  padding: 20px;
  background-color: #f8f9fa;
}

.confirm-card {
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  padding: 40px;
  max-width: 500px;
  width: 100%;
}

.text-success {
  color: #28a745;
}

.text-danger {
  color: #dc3545;
}

.btn {
  padding: 10px 25px;
  border-radius: 5px;
  font-weight: 600;
  text-decoration: none;
  display: inline-block;
}

.btn-primary {
  background-color: #FF6B6B;
  border-color: #FF6B6B;
  color: white;
}

.btn-primary:hover {
  background-color: #ff5252;
  border-color: #ff5252;
}

.btn-outline-secondary {
  background-color: transparent;
  border: 1px solid #6c757d;
  color: #6c757d;
}

.btn-outline-secondary:hover {
  background-color: #6c757d;
  color: white;
}
</style>
