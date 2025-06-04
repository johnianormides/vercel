<template>
  <div class="admin-layout">
    <!-- Sidebar Navigation -->
    <aside class="admin-sidebar">
      <div class="sidebar-header">
        <img src="/Designer.png" alt="Logo" class="logo-img" />
        <span class="logo-text">PAWFECT</span>
      </div>

      <nav class="sidebar-nav">
        <router-link to="/admin/dashboard" class="nav-item" active-class="active">
          <i class="fas fa-chart-line"></i>
          <span>Dashboard</span>
        </router-link>
        <router-link to="/admin/pets" class="nav-item" :class="{ 'active': $route.path.includes('/admin/pets') }">
          <i class="fas fa-paw"></i>
          <span>Pets</span>
        </router-link>
        <router-link to="/admin/applications" class="nav-item" active-class="active">
          <i class="fas fa-file-alt"></i>
          <span>Applications</span>
        </router-link>
        <router-link to="/admin/pet-history" class="nav-item" active-class="active">
          <i class="fas fa-history"></i>
          <span>Pet History</span>
        </router-link>
      </nav>

      <div class="sidebar-footer">
        <a href="#" @click.prevent="handleLogout" class="nav-item">
          <i class="fas fa-sign-out-alt"></i>
          <span>Logout</span>
        </a>
      </div>
    </aside>

    <!-- Main Content -->
    <main class="admin-main">
      <header class="admin-header">
        <div class="header-left">
          <h1>Pet Details</h1>
          <router-link to="/admin/pets" class="back-link">
            <i class="fas fa-arrow-left"></i> Back to Pets
          </router-link>
        </div>
        <div class="header-right">
          <div class="admin-profile">
            <img src="/Designer.png" alt="Admin" class="admin-avatar" />
            <span class="admin-name">Admin</span>
          </div>
        </div>
      </header>

      <div class="content-wrapper">
        <div v-if="loading" class="loading-container">
          <div class="loading-spinner"></div>
          <p>Loading pet details...</p>
        </div>

        <div v-else-if="error" class="error-container">
          <i class="fas fa-exclamation-triangle"></i>
          <p>{{ error }}</p>
          <router-link to="/admin/pets" class="return-link">Return to Pets List</router-link>
        </div>

        <div v-else-if="pet" class="pet-profile">
          <div class="profile-header">
            <div class="pet-image-wrapper">
              <img :src="pet.photoUrl || '/Img/default-pet.jpg'" :alt="pet.name" class="pet-image">
              <input
                type="file"
                ref="photoInput"
                @change="handlePhotoChange"
                accept="image/*"
                class="hidden-input"
              >

            </div>
            <div class="pet-info">
              <div class="pet-name-status">
                <h2>{{ pet.name }}</h2>
                <span class="status-badge" :class="getStatusClass(pet.status)">
                  {{ pet.status }}
                </span>
              </div>
              <div class="pet-attributes">
                <div class="attribute">
                  <i class="fas fa-paw"></i>
                  <span>{{ pet.type }}</span>
                </div>
                <div class="attribute">
                  <i class="fas fa-dog"></i>
                  <span>{{ pet.breed }}</span>
                </div>
                <div class="attribute">
                  <i class="fas fa-birthday-cake"></i>
                  <span>{{ pet.age }}</span>
                </div>
                <div class="attribute">
                  <i class="fas fa-venus-mars"></i>
                  <span>{{ pet.gender }}</span>
                </div>
              </div>
              <div class="pet-description">
                <h3><i class="fas fa-info-circle"></i> About {{ pet.name }}</h3>
                <p class="info-text">{{ pet.description || 'No description available.' }}</p>
              </div>
              <div class="quick-actions">
                <button @click="editPet" class="primary-btn">
                  <i class="fas fa-edit"></i> Edit Details
                </button>
                <button @click="confirmDelete" class="danger-btn">
                  <i class="fas fa-trash"></i> Delete
                </button>
                <button @click="changeStatus('On Hold')" v-if="pet.status !== 'On Hold'" class="status-btn-small hold">
                  <i class="fas fa-pause-circle"></i> Put on Hold
                </button>
                <button @click="changeStatus('Adopted')" v-if="pet.status !== 'Adopted'" class="status-btn-small adopted">
                  <i class="fas fa-home"></i> Mark as Adopted
                </button>
              </div>
            </div>
          </div>

          <!-- <div class="info-tabs">
            <div class="tab-container">
              <div class="tab-content">
                <div class="info-section">
                  <h3><i class="fas fa-info-circle"></i> About {{ pet.name }}</h3>
                  <p class="info-text">{{ pet.description || 'No description available.' }}</p>
                </div>
              </div>
            </div>
          </div> -->
        </div>

        <!-- Delete Confirmation Modal -->
        <div v-if="showDeleteModal" class="modal-overlay" @click.self="showDeleteModal = false">
          <div class="modal">
            <div class="modal-header">
              <h3>Confirm Delete</h3>
              <button class="close-btn" @click="showDeleteModal = false">
                <i class="fas fa-times"></i>
              </button>
            </div>
            <div class="modal-body">
              <i class="fas fa-exclamation-triangle warning-icon"></i>
              <p>Are you sure you want to delete <strong>{{ pet?.name }}</strong>?</p>
              <p class="warning-text">This action cannot be undone.</p>
            </div>
            <div class="modal-actions">
              <button class="cancel-btn" @click="showDeleteModal = false">Cancel</button>
              <button class="delete-btn" @click="deletePet">Delete</button>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
export default {
  name: 'AdminViewPet',
  data() {
    return {
      pet: null,
      loading: true,
      error: null,
      showDeleteModal: false
    }
  },
  computed: {
    petId() {
      return this.$route.params.id
    }
  },
  mounted() {
    this.fetchPetDetails()
  },
  methods: {
    handleLogout() {
      // Clear auth data from localStorage
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      // Redirect to login
      this.$router.push('/admin-login')
    },

    async fetchPetDetails() {
      this.loading = true
      try {
        const response = await fetch(`http://localhost:5000/api/pet/${this.petId}`)

        if (!response.ok) {
          throw new Error(`Failed to fetch pet details: ${response.status}`)
        }

        const result = await response.json()

        if (result.success && result.data) {
          this.pet = {
            id: result.data.id,
            name: result.data.name,
            type: result.data.species,
            breed: result.data.breed,
            age: result.data.age,
            gender: result.data.gender,
            photoUrl: result.data.photo_url,
            description: result.data.description,
            personality: result.data.personality,
            vaccinated: result.data.vaccinated || false,
            neutered: result.data.neutered || false,
            specialNeeds: result.data.special_needs || false,
            medicalInfo: result.data.medical_info,
            history: result.data.history,
            status: result.data.status || 'Available'
          }
        } else {
          throw new Error(result.message || 'Failed to fetch pet details')
        }
      } catch (error) {
        console.error('Error fetching pet details:', error)
        this.error = error.message || 'Failed to load pet details. Please try again.'
      } finally {
        this.loading = false
      }
    },

    getStatusClass(status) {
      switch (status?.toLowerCase()) {
        case 'available': return 'status-available'
        case 'on hold': return 'status-hold'
        case 'adopted': return 'status-adopted'
        default: return 'status-unknown'
      }
    },

    editPet() {
      this.$router.push(`/admin/pets/edit/${this.petId}`)
    },

    confirmDelete() {
      this.showDeleteModal = true
    },

    async deletePet() {
      try {
        const response = await fetch(`http://localhost:5000/api/pet/${this.petId}`, {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json'
          }
        })

        if (!response.ok) {
          throw new Error(`Failed to delete pet: ${response.status}`)
        }

        const result = await response.json()

        if (result.success) {
          alert(`${this.pet.name} has been successfully deleted.`)
          this.$router.push('/admin/pets')
        } else {
          throw new Error(result.message || 'Failed to delete pet')
        }
      } catch (error) {
        console.error('Error deleting pet:', error)
        alert(`Error deleting pet: ${error.message}`)
      } finally {
        this.showDeleteModal = false
      }
    },

    async changeStatus(newStatus) {
      try {
        const response = await fetch(`http://localhost:5000/api/pet/${this.petId}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            status: newStatus
          })
        })

        if (!response.ok) {
          throw new Error(`Failed to update pet status: ${response.status}`)
        }

        const result = await response.json()

        if (result.success) {
          this.pet.status = newStatus
          alert(`Status for ${this.pet.name} has been updated to ${newStatus}.`)
        } else {
          throw new Error(result.message || 'Failed to update pet status')
        }
      } catch (error) {
        console.error('Error updating pet status:', error)
        alert(`Error updating pet status: ${error.message}`)
      }
    },

    changePhoto() {
      // This method is no longer needed as we're using triggerPhotoInput
    },

    triggerPhotoInput() {
      this.$refs.photoInput.click()
    },

    async handlePhotoChange(event) {
      const file = event.target.files[0]
      if (!file) return

      try {
        const formData = new FormData()
        formData.append('photo', file)

        const response = await fetch(`http://localhost:5000/api/pet/${this.petId}/photo`, {
          method: 'PUT',
          body: formData
        })

        if (!response.ok) {
          throw new Error(`Failed to update photo: ${response.status}`)
        }

        const result = await response.json()

        if (result.success) {
          // Update the pet's photo URL in the local state
          this.pet.photoUrl = result.data.photo_url
          alert('Photo updated successfully!')
        } else {
          throw new Error(result.message || 'Failed to update photo')
        }
      } catch (error) {
        console.error('Error updating photo:', error)
        alert(`Error updating photo: ${error.message}`)
      }
    }
  }
}
</script>

<style scoped>
.admin-layout {
  display: flex;
  min-height: 100vh;
  background: #f4f6fa;
}

.admin-sidebar {
  width: 260px;
  background: #fff;
  border-right: 1px solid #e0e0e0;
  display: flex;
  flex-direction: column;
  position: fixed;
  height: 100vh;
  left: 0;
  top: 0;
  z-index: 1000;
}

.sidebar-header {
  padding: 1.5rem;
  display: flex;
  align-items: center;
  gap: 0.8rem;
  border-bottom: 1px solid #e0e0e0;
}

.logo-img {
  width: 32px;
  height: 32px;
}

.logo-text {
  font-size: 1.2rem;
  font-weight: 700;
  color: #f7871f;
}

.sidebar-nav {
  flex: 1;
  padding: 1rem 0;
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  padding: 0.8rem 1.5rem;
  color: #666;
  text-decoration: none;
  transition: all 0.3s ease;
  font-size: 0.95rem;
}

.nav-item:hover {
  background: #f8f9fa;
  color: #f7871f;
  padding-left: 1.8rem;
}

.nav-item.active {
  background: #fff5eb;
  color: #f7871f;
  border-left: 3px solid #f7871f;
  font-weight: 500;
}

.nav-item i {
  width: 20px;
  text-align: center;
  font-size: 1.1rem;
}

.sidebar-footer {
  padding: 1rem 0;
  border-top: 1px solid #e0e0e0;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.admin-main {
  flex: 1;
  margin-left: 260px;
  padding: 0;
  background: #f4f6fa;
  padding-top: 70px; /* Add padding to account for the fixed header */
}

.admin-header {
  background: #fff;
  padding: 1rem 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #e0e0e0;
  box-shadow: 0 2px 4px rgba(0,0,0,0.03);
  position: fixed;
  top: 0;
  right: 0;
  left: 260px;
  z-index: 100;
  height: 70px;
}

.header-left h1 {
  font-size: 1.5rem;
  color: #333;
  margin: 0;
}

.back-link {
  color: #f7871f;
  text-decoration: none;
  font-size: 0.9rem;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  transition: color 0.3s ease;
}

.back-link:hover {
  color: #e67012;
}

.back-link i {
  font-size: 0.8rem;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 0.8rem;
}

.admin-profile {
  display: flex;
  align-items: center;
  gap: 0.8rem;
}

.admin-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
}

.admin-name {
  font-weight: 500;
  color: #333;
}

.content-wrapper {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.loading-container, .error-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem 0;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
  text-align: center;
}

.loading-spinner {
  border: 4px solid #f3f3f3;
  border-top: 4px solid #f7871f;
  border-radius: 50%;
  width: 44px;
  height: 44px;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error-container i {
  color: #e74c3c;
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.return-link {
  margin-top: 1rem;
  color: #f7871f;
  text-decoration: none;
  font-weight: 500;
}

/* Pet Profile Styling */
.pet-profile {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.profile-header {
  display: flex;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
  overflow: hidden;
}

.pet-image-wrapper {
  width: 280px;
  height: auto;
  flex-shrink: 0;
  overflow: visible;
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  padding: 1.5rem;
  align-items: center;
}

.pet-image {
  width: calc(100% - 2rem);
  height: 280px;
  object-fit: cover;
  border-radius: 8px;
  margin: 0 1rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.hidden-input {
  display: none;
}

.change-photo-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.8rem 1rem;
  background: #f7871f;
  color: white;
  border: none;
  border-radius: 6px;
  font-weight: 500;
  font-size: 0.95rem;
  cursor: pointer;
  transition: background 0.2s;
  width: 100%;
}

.change-photo-btn:hover {
  background: #e67012;
}

.change-photo-btn i {
  margin-right: 0.5rem;
}

.pet-info {
  flex: 1;
  padding: 2rem;
  display: flex;
  flex-direction: column;
}

.pet-name-status {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0.5rem;
}

.pet-name-status h2 {
  font-size: 2rem;
  font-weight: 600;
  color: #333;
  margin: 0;
}

.status-badge {
  display: inline-block;
  padding: 0.5rem 1rem;
  border-radius: 30px;
  font-weight: 500;
  font-size: 0.9rem;
}

.status-available {
  background: #e8f5e9;
  color: #2e7d32;
}

.status-hold {
  background: #fff3e0;
  color: #e65100;
}

.status-adopted {
  background: #e3f2fd;
  color: #0d47a1;
}

.status-unknown {
  background: #f5f5f5;
  color: #757575;
}

.pet-attributes {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-bottom: 0.5rem;
}

.attribute {
  display: flex;
  align-items: center;
  background: #f8f9fa;
  padding: 0.6rem 1.2rem;
  border-radius: 8px;
  font-size: 1rem;
}

.attribute i {
  margin-right: 0.8rem;
  color: #f7871f;
  font-size: 1.1rem;
}

.pet-description {
  margin: 1.5rem 0;
}

.pet-description h3 {
  font-size: 1.2rem;
  font-weight: 600;
  color: #333;
  margin: 0 0 0.8rem 0;
  display: flex;
  align-items: center;
}

.pet-description h3 i {
  margin-right: 0.8rem;
  color: #f7871f;
}

.pet-description .info-text {
  font-size: 1rem;
  line-height: 1.6;
  color: #555;
  margin: 0;
}

.quick-actions {
  display: flex;
  gap: 0.8rem;
  margin-top: auto;
  flex-wrap: wrap;
  align-items: center;
}

.primary-btn, .danger-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.8rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-weight: 500;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.primary-btn {
  background: #f7871f;
  color: white;
}

.primary-btn:hover {
  background: #e67012;
}

.danger-btn {
  background: #ffebee;
  color: #f44336;
}

.danger-btn:hover {
  background: #ffcdd2;
}

.primary-btn i, .danger-btn i {
  margin-right: 0.6rem;
}

.status-btn-small {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.6rem 1rem;
  border: none;
  border-radius: 6px;
  font-weight: 500;
  font-size: 0.85rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.status-btn-small i {
  margin-right: 0.4rem;
  font-size: 0.9rem;
}

.status-btn-small.hold {
  background: #fff3e0;
  color: #e65100;
}

.status-btn-small.hold:hover {
  background: #ffe0b2;
}

.status-btn-small.adopted {
  background: #e3f2fd;
  color: #0d47a1;
}

.status-btn-small.adopted:hover {
  background: #bbdefb;
}

/* Info Tabs Styling */
.info-tabs {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
  overflow: hidden;
}

.tab-container {
  padding: 1.5rem;
}

.info-section {
  margin-bottom: 2rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid #eee;
}

.info-section:last-child {
  margin-bottom: 0;
  padding-bottom: 0;
  border-bottom: none;
}

.info-section h3 {
  font-size: 1.3rem;
  font-weight: 600;
  color: #333;
  margin: 0 0 1rem 0;
  display: flex;
  align-items: center;
}

.info-section h3 i {
  margin-right: 0.8rem;
  color: #f7871f;
}

.info-text {
  font-size: 1rem;
  line-height: 1.6;
  color: #555;
  margin: 0;
}

.health-indicators {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-bottom: 1.2rem;
}

.health-indicator {
  display: flex;
  align-items: center;
  padding: 0.6rem 1.2rem;
  border-radius: 8px;
  background: #f5f5f5;
  color: #757575;
  font-size: 0.95rem;
}

.health-indicator.active {
  background: #e8f5e9;
  color: #2e7d32;
}

.health-indicator i {
  margin-right: 0.6rem;
}

/* Status Actions Styling */
.status-actions {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
  padding: 1.5rem;
}

.status-actions h3 {
  font-size: 1.2rem;
  font-weight: 600;
  color: #333;
  margin: 0 0 1.2rem 0;
}

.status-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}

.status-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.8rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-weight: 500;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.status-btn i {
  margin-right: 0.6rem;
}

.status-btn.available {
  background: #e8f5e9;
  color: #2e7d32;
}

.status-btn.available:hover {
  background: #c8e6c9;
}

.status-btn.hold {
  background: #fff3e0;
  color: #e65100;
}

.status-btn.hold:hover {
  background: #ffe0b2;
}

.status-btn.adopted {
  background: #e3f2fd;
  color: #0d47a1;
}

.status-btn.adopted:hover {
  background: #bbdefb;
}

/* Modal Styling */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal {
  background: #fff;
  border-radius: 12px;
  width: 100%;
  max-width: 450px;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.15);
  overflow: hidden;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.2rem 1.5rem;
  border-bottom: 1px solid #eee;
}

.modal-header h3 {
  margin: 0;
  color: #333;
  font-size: 1.3rem;
}

.close-btn {
  background: none;
  border: none;
  color: #999;
  font-size: 1.2rem;
  cursor: pointer;
  padding: 0.3rem;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: color 0.2s;
}

.close-btn:hover {
  color: #333;
}

.modal-body {
  padding: 1.5rem;
  text-align: center;
}

.warning-icon {
  font-size: 3rem;
  color: #f44336;
  margin-bottom: 1rem;
}

.modal-body p {
  margin: 0 0 0.8rem 0;
  font-size: 1.1rem;
  color: #333;
}

.warning-text {
  color: #f44336;
  font-size: 0.95rem;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  padding: 1.2rem 1.5rem;
  border-top: 1px solid #eee;
}

.cancel-btn, .delete-btn {
  padding: 0.8rem 1.5rem;
  border-radius: 8px;
  font-weight: 500;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.2s;
}

.cancel-btn {
  background: #f5f5f5;
  color: #666;
  border: none;
}

.cancel-btn:hover {
  background: #e0e0e0;
}

.delete-btn {
  background: #f44336;
  color: white;
  border: none;
}

.delete-btn:hover {
  background: #d32f2f;
}

@media (max-width: 992px) {
  .profile-header {
    flex-direction: column;
  }

  .pet-image-wrapper {
    width: 100%;
    height: 240px;
  }

  .pet-info {
    padding: 1.5rem;
  }

  .pet-description {
    margin: 1.2rem 0;
  }
}

@media (max-width: 768px) {
  .admin-sidebar {
    width: 70px;
  }
  .sidebar-header {
    padding: 1rem;
  }
  .logo-text {
    display: none;
  }
  .nav-item span {
    display: none;
  }
  .nav-item {
    justify-content: center;
    padding: 1rem;
  }
  .admin-main {
    margin-left: 70px;
  }
  .admin-header {
    left: 70px;
  }
  .content-wrapper {
    padding: 1.5rem 1rem;
  }
  .pet-name-status {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.8rem;
  }
  .quick-actions {
    flex-direction: column;
  }
  .status-buttons {
    flex-direction: column;
  }
}

@media (max-width: 576px) {
  .pet-attributes {
    flex-direction: column;
  }
  .health-indicators {
    flex-direction: column;
  }
  .header-left h1 {
    font-size: 1.2rem;
  }
  .admin-name {
    display: none;
  }
}
</style>
