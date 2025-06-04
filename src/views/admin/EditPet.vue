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
          <h1>{{ isNewPet ? 'Add New Pet' : 'Edit Pet' }}</h1>
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
      <div class="edit-pet-container">

        <div v-if="loading" class="loading-container">
          <div class="loading-spinner"></div>
          <p>Loading pet details...</p>
        </div>

        <div v-else-if="error" class="error-container">
          <i class="fas fa-exclamation-triangle"></i>
          <p>{{ error }}</p>
          <router-link to="/admin/pets" class="return-link">Return to Pets List</router-link>
        </div>

        <form v-else @submit.prevent="savePet" class="pet-form redesigned-form">
          <div class="form-row photo-info-row">
            <!-- Photo Card (left) -->
            <section class="form-card photo-card">
              <h2><i class="fas fa-camera"></i> Pet Photo</h2>
              <div class="photo-upload redesigned-photo-upload">
                <div class="current-photo large-preview">
                  <img :src="petForm.photoPreview || petForm.photoUrl || '/Img/default-pet.jpg'" alt="Pet Photo Preview">
                  <button v-if="petForm.photoUrl || petForm.photoPreview" type="button" class="remove-photo-x" @click="clearPhoto">
                    <i class="fas fa-times"></i>
                  </button>
                </div>
                <div class="upload-controls below-image-upload">
                  <input type="file" id="pet-photo" @change="handlePhotoUpload" accept="image/*" class="file-input">
                  <label v-if="!petForm.photoUrl && !petForm.photoPreview" for="pet-photo" class="upload-btn small-upload-btn">
                    <i class="fas fa-upload"></i> Add Photo
                  </label>
                  <label v-else for="pet-photo" class="upload-btn small-upload-btn">
                    <i class="fas fa-upload"></i> Change Photo
                  </label>
                </div>
              </div>
            </section>
            <!-- Basic Info Card (right) -->
            <section class="form-card info-card">
              <h2><i class="fas fa-info-circle"></i> Basic Information</h2>
              <div class="form-row">
                <div class="form-group">
                  <label for="pet-name">Name <span class="required">*</span></label>
                  <input type="text" id="pet-name" v-model="petForm.name" required placeholder="Enter pet name">
                </div>
                <div class="form-group">
                  <label for="pet-type">Type <span class="required">*</span></label>
                  <select id="pet-type" v-model="petForm.type" required>
                    <option value="">Select type</option>
                    <option value="Dog">Dog</option>
                    <option value="Cat">Cat</option>
                    <option value="Bird">Bird</option>
                    <option value="Small Animal">Small Animal</option>
                    <option value="Other">Other</option>
                  </select>
                </div>
              </div>
              <div class="form-row">
                <div class="form-group">
                  <label for="pet-breed">Breed <span class="required">*</span></label>
                  <input type="text" id="pet-breed" v-model="petForm.breed" required placeholder="Enter breed">
                </div>
                <div class="form-group">
                  <label for="pet-age">Age <span class="required">*</span></label>
                  <input type="text" id="pet-age" v-model="petForm.age" required placeholder="e.g., 2 years">
                </div>
                <div class="form-group">
                  <label for="pet-gender">Gender <span class="required">*</span></label>
                  <select id="pet-gender" v-model="petForm.gender" required>
                    <option value="">Select gender</option>
                    <option value="Male">Male</option>
                    <option value="Female">Female</option>
                  </select>
                </div>
                <div class="form-group">
                  <label for="pet-status">Status <span class="required">*</span></label>
                  <select id="pet-status" v-model="petForm.status" required>
                    <option value="Available">Available</option>
                    <option value="On Hold">On Hold</option>
                    <option value="Adopted">Adopted</option>
                  </select>
                </div>
              </div>
            </section>
          </div>
          <!-- Description Section -->
           <section class="form-card">
            <h2><i class="fas fa-align-left"></i> Description</h2>
            <div class="form-row">
              <div class="form-group full-width">
                <label for="pet-description">Description</label>
                <textarea id="pet-description" v-model="petForm.description" rows="3" placeholder="Enter a description of the pet"></textarea>
              </div>
            </div>
          </section>
          <!-- Health Card -->
          <!-- <section class="form-card">
            <h2><i class="fas fa-medkit"></i> Health Information</h2>
            <div class="form-checkboxes">
              <div class="form-checkbox">
                <input type="checkbox" id="pet-vaccinated" v-model="petForm.vaccinated">
                <label for="pet-vaccinated">Vaccinated</label>
              </div>
              <div class="form-checkbox">
                <input type="checkbox" id="pet-neutered" v-model="petForm.neutered">
                <label for="pet-neutered">Neutered/Spayed</label>
              </div>
              <div class="form-checkbox">
                <input type="checkbox" id="pet-special-needs" v-model="petForm.specialNeeds">
                <label for="pet-special-needs">Special Needs</label>
              </div>
            </div>
            <div class="form-row">
              <div class="form-group full-width">
                <label for="pet-medical-info">Medical Information</label>
                <textarea id="pet-medical-info" v-model="petForm.medicalInfo" rows="2" placeholder="Enter any medical information"></textarea>
              </div>
            </div>
          </section> -->
          <!-- Background Card -->
          <!-- <section class="form-card">
            <h2><i class="fas fa-history"></i> Background</h2>
            <div class="form-row">
              <div class="form-group full-width">
                <label for="pet-history">Pet History</label>
                <textarea id="pet-history" v-model="petForm.history" rows="2" placeholder="Enter any background or history information"></textarea>
              </div>
            </div>
          </section> -->
          <!-- Sticky Actions -->
          <div class="form-actions sticky-actions">
            <router-link to="/admin/pets" class="cancel-btn">Cancel</router-link>
            <button type="submit" class="save-btn">
              <i class="fas fa-save"></i> {{ isNewPet ? 'Add Pet' : 'Save Changes' }}
            </button>
          </div>
        </form>
      </div>
    </main>
  </div>
</template>

<script>
export default {
  name: 'AdminEditPet',
  data() {
    return {
      petForm: {
        name: '',
        type: '',
        breed: '',
        age: '',
        gender: '',
        photoUrl: '',
        photoPreview: null,
        photoFile: null,
        description: '',
        vaccinated: false,
        neutered: false,
        specialNeeds: false,
        medicalInfo: '',
        history: '',
        status: 'Available'
      },
      loading: true,
      error: null,
      isSubmitting: false
    }
  },
  computed: {
    petId() {
      return this.$route.params.id
    },
    isNewPet() {
      return !this.petId
    }
  },
  mounted() {
    if (!this.isNewPet) {
      this.fetchPetDetails()
    } else {
      this.loading = false
    }
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
          this.petForm = {
            name: result.data.name,
            type: result.data.species,
            breed: result.data.breed,
            age: result.data.age,
            gender: result.data.gender,
            photoUrl: result.data.photo_url,
            photoPreview: null,
            photoFile: null,
            description: result.data.description || '',
            vaccinated: result.data.vaccinated || false,
            neutered: result.data.neutered || false,
            specialNeeds: result.data.special_needs || false,
            medicalInfo: result.data.medical_info || '',
            history: result.data.history || '',
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

    handlePhotoUpload(event) {
      const file = event.target.files[0]
      if (!file) return

      this.petForm.photoFile = file

      // Create a preview
      const reader = new FileReader()
      reader.onload = e => {
        this.petForm.photoPreview = e.target.result
      }
      reader.readAsDataURL(file)
    },

    clearPhoto() {
      this.petForm.photoUrl = ''
      this.petForm.photoPreview = null
      this.petForm.photoFile = null

      // Clear the file input
      const fileInput = document.getElementById('pet-photo')
      if (fileInput) fileInput.value = ''
    },

    async savePet() {
      if (this.isSubmitting) return
      this.isSubmitting = true
      this.error = null

      try {
        // First, handle photo upload if there's a new photo
        let photoUrl = this.petForm.photoUrl
        if (this.petForm.photoFile) {
          const formData = new FormData()
          formData.append('file', this.petForm.photoFile)

          try {
            // Get admin session token
            const adminSession = localStorage.getItem('adminSession')
            if (!adminSession) {
              throw new Error("You're not logged in as an admin")
            }

            // Upload the photo first
            const uploadResponse = await fetch('http://localhost:5000/api/upload', {
              method: 'POST',
              headers: {
                'Authorization': `Bearer ${adminSession}`
              },
              body: formData
            })

            if (!uploadResponse.ok) {
              throw new Error(`Photo upload failed: ${uploadResponse.status}`)
            }

            const uploadResult = await uploadResponse.json()
            if (!uploadResult.success) {
              throw new Error(uploadResult.message || 'Photo upload failed')
            }

            // Get the uploaded photo URL
            photoUrl = uploadResult.data.url
          } catch (uploadError) {
            console.error('Error uploading photo:', uploadError)
            throw new Error(`Failed to upload photo: ${uploadError.message}`)
          }
        }

        // Prepare the pet data for API
        const petData = {
          name: this.petForm.name,
          species: this.petForm.type,
          breed: this.petForm.breed,
          age: this.petForm.age,
          gender: this.petForm.gender,
          description: this.petForm.description,
          status: this.petForm.status
        }

        // Add the photo URL if available
        if (photoUrl) {
          petData.photo_url = photoUrl
        }

        // Get admin session token
        const adminSession = localStorage.getItem('adminSession')
        if (!adminSession) {
          throw new Error("You're not logged in as an admin")
        }

        const url = this.isNewPet
          ? 'http://localhost:5000/api/pet'
          : `http://localhost:5000/api/pet/${this.petId}`

        const method = this.isNewPet ? 'POST' : 'PUT'

        // Send the request to create or update the pet
        const response = await fetch(url, {
          method: method,
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${adminSession}`
          },
          body: JSON.stringify(petData)
        })

        if (!response.ok) {
          const errorData = await response.json()
          throw new Error(errorData.message || `Failed to ${this.isNewPet ? 'create' : 'update'} pet: ${response.status}`)
        }

        const result = await response.json()

        if (result.success) {
          // Show success message
          alert(`Pet ${this.isNewPet ? 'created' : 'updated'} successfully!`)
          
          // Redirect to pets list or view page
          this.$router.push('/admin/pets')
        } else {
          throw new Error(result.message || `Failed to ${this.isNewPet ? 'create' : 'update'} pet`)
        }
      } catch (error) {
        console.error(`Error ${this.isNewPet ? 'creating' : 'updating'} pet:`, error)
        this.error = error.message || `Error ${this.isNewPet ? 'creating' : 'updating'} pet`
        alert(this.error)
      } finally {
        this.isSubmitting = false
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
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
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
  padding: 2rem;
}

.admin-header {
  background: #fff;
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #e0e0e0;
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

.edit-pet-container {
  max-width: 1100px;
}

.page-header, .pet-profile-card, .form-section, .form-container, .pet-details-container {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

.page-header {
  display: flex;
  align-items: center;
  margin-bottom: 28px;
  padding: 18px 28px;
}

.header-navigation {
  display: flex;
  align-items: center;
  width: 100%;
}

.back-button {
  color: #f7871f;
  text-decoration: none;
  margin-right: 22px;
  display: flex;
  align-items: center;
  font-weight: 500;
  font-size: 1.05rem;
  transition: color 0.2s;
}

.back-button i {
  margin-right: 7px;
}

.back-button:hover {
  color: #e67012;
}

.loading-container, .error-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 48px 0;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
  margin-top: 24px;
}

.loading-spinner {
  border: 4px solid #f3f3f3;
  border-top: 4px solid #f7871f;
  border-radius: 50%;
  width: 44px;
  height: 44px;
  animation: spin 1s linear infinite;
  margin-bottom: 18px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error-container i {
  color: #e74c3c;
  font-size: 2.5rem;
  margin-bottom: 12px;
}

.return-link {
  margin-top: 12px;
  color: #f7871f;
  text-decoration: none;
  font-weight: 500;
}

.pet-form {
  margin-top: 18px;
}

.form-container {
  display: flex;
  gap: 24px;
  margin-bottom: 22px;
}

.form-section {
  padding: 24px 22px 18px 22px;
}

.form-section.full-width {
  width: 100%;
}

.form-section h3 {
  margin: 0 0 18px 0;
  color: #f7871f;
  font-size: 1.13rem;
  display: flex;
  align-items: center;
  border-bottom: 1px solid #ffe2cc;
  padding-bottom: 8px;
  font-weight: 600;
}

.form-section h3 i {
  margin-right: 8px;
  color: #f7871f;
}

.form-group {
  margin-bottom: 14px;
}

.form-row {
  display: flex;
  gap: 14px;
  margin-bottom: 14px;
}

.form-row .form-group {
  flex: 1;
  margin-bottom: 0;
}

label {
  display: block;
  margin-bottom: 5px;
  font-weight: 500;
  color: #222;
  font-size: 0.98rem;
}

.required {
  color: #e74c3c;
}

input[type="text"],
input[type="number"],
select,
textarea {
  width: 100%;
  padding: 10px 12px;
  border: 1.5px solid #e0e0e0;
  border-radius: 6px;
  font-size: 0.97rem;
  background: #fafbfc;
  transition: border-color 0.2s, box-shadow 0.2s;
  box-sizing: border-box;
}

input[type="text"]:focus,
input[type="number"]:focus,
select:focus,
textarea:focus {
  border-color: #f7871f;
  outline: none;
  background: #fff;
  box-shadow: 0 0 0 2px #ffe2cc;
}

textarea {
  resize: vertical;
  min-height: 80px;
}

.photo-upload {
  display: flex;
  gap: 18px;
  align-items: center;
}

.current-photo {
  width: 120px;
  height: 120px;
  border-radius: 10px;
  overflow: hidden;
  border: 1.5px solid #e0e0e0;
  background: #fff;
  box-shadow: 0 1px 4px rgba(0,0,0,0.04);
}

.current-photo img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.upload-controls {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.file-input {
  display: none;
}

.upload-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: #f7871f;
  color: #fff;
  padding: 8px 18px;
  border-radius: 5px;
  cursor: pointer;
  font-weight: 500;
  font-size: 1rem;
  border: none;
  transition: background 0.2s;
  width: fit-content;
}

.upload-btn:hover {
  background: #e67012;
}

.upload-btn i {
  margin-right: 6px;
}

.clear-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: #e74c3c;
  color: #fff;
  border: none;
  padding: 8px 18px;
  border-radius: 5px;
  cursor: pointer;
  font-weight: 500;
  font-size: 1rem;
  transition: background 0.2s;
  width: fit-content;
}

.clear-btn:hover {
  background: #c0392b;
}

.clear-btn i {
  margin-right: 6px;
}

.form-checkboxes {
  display: flex;
  gap: 18px;
  margin-bottom: 12px;
}

.form-checkbox {
  display: flex;
  align-items: center;
  font-size: 0.97rem;
}

.form-checkbox input[type="checkbox"] {
  margin-right: 6px;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 14px;
  margin-top: 28px;
}

.cancel-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: #7f8c8d;
  color: #fff;
  text-decoration: none;
  padding: 10px 22px;
  border-radius: 5px;
  cursor: pointer;
  font-weight: 500;
  font-size: 1rem;
  transition: background 0.2s;
}

.cancel-btn:hover {
  background: #7f8c8d;
}

.save-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: #f7871f;
  color: #fff;
  border: none;
  padding: 10px 22px;
  border-radius: 5px;
  cursor: pointer;
  font-weight: 500;
  font-size: 1rem;
  transition: background 0.2s;
}

.save-btn:hover {
  background: #e67012;
}

.save-btn i {
  margin-right: 8px;
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
    padding: 18px 8px 8px 8px;
  }
}

/**** Redesigned Form Styles ****/
.redesigned-form {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}
.form-card {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
  padding: 2rem 2rem 1.5rem 2rem;
  margin-bottom: 0;
}
.form-card h2 {
  font-size: 1.2rem;
  color: #f7871f;
  margin-bottom: 1.2rem;
  display: flex;
  align-items: center;
  gap: 0.7rem;
  font-weight: 700;
}
.form-row {
  display: flex;
  gap: 1.5rem;
  margin-bottom: 1.2rem;
}
.form-group {
  flex: 1;
  display: flex;
  flex-direction: column;
  margin-bottom: 0;
}
.form-group.full-width {
  flex: 2;
}
.required {
  color: #e74c3c;
  margin-left: 2px;
}
.redesigned-photo-upload {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex-direction: column;
}
.current-photo.large-preview {
  width: 160px;
  height: 160px;
  border-radius: 12px;
  overflow: hidden;
  border: 1.5px solid #eee;
  background: #fafbfc;
  box-shadow: 0 1px 4px rgba(0,0,0,0.04);
}
.current-photo.large-preview img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.sticky-actions {
  position: sticky;
  bottom: 0;
  background: #fff;
  padding: 1.2rem 2rem 1.2rem 2rem;
  border-radius: 0 0 12px 12px;
  box-shadow: 0 -2px 8px rgba(0,0,0,0.03);
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  z-index: 10;
}
/**** End Redesigned Form Styles ****/

.photo-info-row {
  display: flex;
  gap: 2rem;
  margin-bottom: 0rem;
}
.photo-card {
  flex: 0 0 260px;
  max-width: 260px;
  min-width: 200px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
}
.info-card {
  flex: 1;
  min-width: 0;
}
@media (max-width: 900px) {
  .photo-info-row {
    flex-direction: column;
    gap: 1.5rem;
  }
  .photo-card, .info-card {
    max-width: 100%;
    min-width: 0;
  }
}

.small-upload-btn {
  padding: 6px 14px;
  font-size: 0.95rem;
  border-radius: 6px;
  min-width: 0;
  width: auto;
  margin-top: 0.5rem;
}
.remove-photo-x {
  position: absolute;
  top: 6px;
  right: 6px;
  background: #e74c3c;
  color: #fff;
  border: none;
  border-radius: 50%;
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1rem;
  cursor: pointer;
  box-shadow: 0 2px 6px rgba(0,0,0,0.08);
  z-index: 2;
  transition: background 0.2s;
}
.remove-photo-x:hover {
  background: #c0392b;
}
.current-photo.large-preview {
  position: relative;
}

.below-image-upload {
  display: flex;
  flex-direction: column;
  align-items: center;
}

</style>
