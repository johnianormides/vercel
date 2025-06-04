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
      <div class="add-pet-container">
        <div class="form-header">
          <div class="header-left">
            <h2>Add New Pet</h2>
            <router-link to="/admin/pets" class="back-link">
              <i class="fas fa-arrow-left"></i> Back to Pets
            </router-link>
          </div>
        </div>

        <form @submit.prevent="handleSubmit" class="pet-form redesigned-form">
          <!-- Basic Info Card -->
          <div class="form-row photo-info-row">
            <!-- Photo Card (left) -->
            <section class="form-card photo-card">
              <h2><i class="fas fa-camera"></i> Pet Photo</h2>
              <div class="photo-upload redesigned-photo-upload">
                <div class="upload-area" @click="triggerFileInput" @dragover.prevent @drop.prevent="handleDrop">
                  <input type="file" ref="fileInput" @change="handleFileSelect" accept="image/*" multiple class="hidden">
                  <div class="upload-content" v-if="!petData.photos.length">
                    <i class="fas fa-cloud-upload-alt"></i>
                    <p>Drag & drop photos here or click to upload</p>
                    <span class="upload-hint">Supports JPG, PNG (max 5MB)</span>
                  </div>
                  <div class="photo-preview" v-else>
                    <div v-for="(photo, index) in petData.photos" :key="index" class="preview-item">
                      <img :src="photo" :alt="'Pet photo ' + (index + 1)">
                      <button type="button" class="remove-photo" @click="removePhoto(index)">
                        <i class="fas fa-times"></i>
                      </button>
                    </div>
                    <div class="add-more" @click="triggerFileInput">
                      <i class="fas fa-plus"></i>
                      <span>Add More</span>
                    </div>
                  </div>
                </div>
              </div>
            </section>

            <!-- Info Card (right) -->
            <section class="form-card info-card">
              <h2><i class="fas fa-info-circle"></i> Basic Information</h2>
              <div class="form-row">
                <div class="form-group">
                  <label for="name">Pet Name <span class="required">*</span></label>
                  <input type="text" id="name" v-model="petData.name" placeholder="Enter pet name" required>
                </div>
                <div class="form-group">
                  <label for="type">Pet Type <span class="required">*</span></label>
                  <select id="type" v-model="petData.type" required>
                    <option value="">Select type</option>
                    <option value="Dog">Dog</option>
                    <option value="Cat">Cat</option>
                    <option value="Bird">Bird</option>
                    <option value="Other">Other</option>
                  </select>
                </div>
              </div>
              <div class="form-row">
                <div class="form-group">
                  <label for="breed">Breed <span class="required">*</span></label>
                  <input type="text" id="breed" v-model="petData.breed" placeholder="Enter breed" required>
                </div>
                <div class="form-group">
                  <label for="age">Age <span class="required">*</span></label>
                  <input type="text" id="age" v-model="petData.age" placeholder="e.g., 2 years" required>
                </div>
              </div>
              <div class="form-row">
                <div class="form-group">
                  <label for="gender">Sex <span class="required">*</span></label>
                  <select id="gender" v-model="petData.gender" required>
                    <option value="">Select gender</option>
                    <option value="Male">Male</option>
                    <option value="Female">Female</option>
                  </select>
                </div>
                <div class="form-group">
                  <label for="status">Status <span class="required">*</span></label>
                  <select id="status" v-model="petData.status" required>
                    <option value="Available">Available</option>
                    <option value="On Hold">On Hold</option>
                    <option value="Adopted">Adopted</option>
                  </select>
                </div>
              </div>
              <div class="form-row">
                <div class="form-group full-width">
                  <label for="description">Description</label>
                  <textarea id="description" v-model="petData.description" rows="4" placeholder="Enter a description of the pet"></textarea>
                </div>
              </div>
            </section>
          </div>

          <div class="error-message" v-if="error">
            {{ error }}
          </div>
          <div class="form-actions sticky-actions">
            <button type="button" class="cancel-btn" @click="cancel" :disabled="isSubmitting">
              Cancel
            </button>
            <button type="submit" class="submit-btn" :disabled="isSubmitting">
              <span v-if="isSubmitting">
                <i class="fas fa-spinner fa-spin"></i> Adding Pet...
              </span>
              <span v-else>Add Pet</span>
            </button>
          </div>
        </form>
      </div>
    </main>
  </div>
</template>

<script>

export default {
  name: 'AddPet',
  data() {
    return {
      isSubmitting: false,
      error: null,
      petData: {
        name: '',
        type: '',
        breed: '',
        age: '',
        gender: '',
        description: '',
        status: 'Available',
        photos: []
      }
    }
  },
  async created() {
    // Check if admin is authenticated
    const adminSession = localStorage.getItem('adminSession')
    const adminUser = localStorage.getItem('adminUser')

    if (!adminSession || !adminUser) {
      this.$router.push('/admin-login')
      return
    }

    try {
      const user = JSON.parse(adminUser)
      if (user.role !== 'admin') {
        this.$router.push('/admin-login')
        return
      }
    } catch (error) {
      console.error('Error checking admin status:', error)
      this.$router.push('/admin-login')
      return
    }
  },
  methods: {
    handleLogout() {
      localStorage.removeItem('adminSession')
      localStorage.removeItem('adminUser')
      this.$router.push('/admin-login')
    },
    triggerFileInput() {
      this.$refs.fileInput.click()
    },
    handleFileSelect(event) {
      const files = event.target.files
      this.processFiles(files)
    },
    handleDrop(event) {
      const files = event.dataTransfer.files
      this.processFiles(files)
    },
    async processFiles(files) {
      for (const file of files) {
        if (file.type.startsWith('image/')) {
          // Check file size (5MB limit)
          if (file.size > 5 * 1024 * 1024) {
            alert('File size must be less than 5MB')
            continue
          }

          try {
            // Get admin session
            const adminSession = localStorage.getItem('adminSession')
            if (!adminSession) {
              throw new Error('Authentication required')
            }

            // Create FormData
            const formData = new FormData()
            formData.append('file', file)

            // Upload through backend API
            const response = await fetch('http://localhost:5000/api/upload', {
              method: 'POST',
              headers: {
                'Authorization': `Bearer ${adminSession}`
              },
              body: formData
            })

            const result = await response.json()

            if (!response.ok) {
              throw new Error(result.message || 'Failed to upload file')
            }

            if (result.success) {
              // Add to photos array
              this.petData.photos.push(result.data.url)
            } else {
              throw new Error(result.message || 'Failed to upload file')
          }
          } catch (error) {
            console.error('Error uploading photo:', error)
            alert(error.message || 'Failed to upload photo. Please try again.')
          }
        } else {
          alert('Please upload only image files (JPG, PNG)')
        }
      }
    },
    removePhoto(index) {
      this.petData.photos.splice(index, 1)
    },
    validateAge(age) {
      // Remove any non-numeric characters except decimal point
      const cleanAge = age.replace(/[^0-9.]/g, '')
      const numAge = parseFloat(cleanAge)

      if (isNaN(numAge) || numAge < 0) {
        throw new Error('Please enter a valid age')
      }

      return numAge
    },
    async handleSubmit() {
      this.isSubmitting = true
      this.error = null

      try {
        // Validate required fields
        if (!this.petData.name || !this.petData.type || !this.petData.breed || !this.petData.age || !this.petData.gender) {
          throw new Error('Please fill in all required fields')
        }

        // Validate at least one photo
        if (this.petData.photos.length === 0) {
          throw new Error('Please upload at least one photo')
        }

        // Validate age
        const validatedAge = this.validateAge(this.petData.age)

        // Get admin session
        const adminSession = localStorage.getItem('adminSession')
        if (!adminSession) {
          throw new Error('Authentication required')
        }

        // Prepare pet data
        const petData = {
              name: this.petData.name,
              species: this.petData.type,
              breed: this.petData.breed,
          age: validatedAge,
          gender: this.petData.gender,
          description: this.petData.description || '',
          status: this.petData.status,
          photo_url: this.petData.photos[0], // Main photo
          photos: this.petData.photos, // All photos
        }

        // Send request to backend
        const response = await fetch('http://localhost:5000/api/pet', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${adminSession}`
          },
          body: JSON.stringify(petData)
        })

        if (!response.ok) {
          const errorData = await response.json()
          throw new Error(errorData.message || 'Failed to add pet')
        }

        const result = await response.json()

        if (result.success) {
        alert('Pet added successfully!')
        this.$router.push('/admin/pets')
        } else {
          throw new Error(result.message || 'Failed to add pet')
        }
      } catch (error) {
        console.error('Error adding pet:', error)
        this.error = error.message || 'Failed to add pet. Please try again.'
      } finally {
        this.isSubmitting = false
      }
    },
    cancel() {
      this.$router.push('/admin/pets')
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
  padding: 2rem;
}

.add-pet-container {
  max-width: 1200px;
  margin: 0 auto;
}

.form-header {
  margin-bottom: 2rem;
}

.form-header h2 {
  color: #222;
  font-size: 1.8rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.subtitle {
  color: #666;
  font-size: 1rem;
}

.header-left {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
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

.redesigned-form {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.form-card {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
  padding: 2rem;
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

.redesigned-photo-upload {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.form-group.full-width {
  grid-column: 1 / -1;
}

.required {
  color: #e74c3c;
  margin-left: 2px;
}

.pet-form {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  padding: 2rem;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
}

.form-section {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 1.5rem;
}

.form-section h3 {
  color: #333;
  font-size: 1.2rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

label {
  display: block;
  color: #555;
  font-weight: 500;
  margin-bottom: 0.5rem;
}

input, select, textarea {
  width: 100%;
  padding: 0.8rem;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  font-size: 0.95rem;
  transition: all 0.3s;
}

input:focus, select:focus, textarea:focus {
  border-color: #f7871f;
  outline: none;
  box-shadow: 0 0 0 3px rgba(247, 135, 31, 0.1);
}

.upload-area {
  border: 2px dashed #e0e0e0;
  border-radius: 12px;
  padding: 2rem;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s;
  width: 100%;
  min-height: 200px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.upload-area:hover {
  border-color: #f7871f;
  background: #fff5eb;
}

.upload-content {
  color: #666;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
}

.upload-content i {
  font-size: 2.5rem;
  color: #f7871f;
  margin-bottom: 1rem;
  opacity: 0.8;
}

.upload-content p {
  font-size: 1rem;
  margin-bottom: 0.5rem;
}

.upload-hint {
  display: block;
  font-size: 0.85rem;
  color: #888;
  margin-top: 0.5rem;
}

.photo-preview {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
  gap: 1rem;
  width: 100%;
}

.preview-item {
  position: relative;
  aspect-ratio: 1;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 6px rgba(0,0,0,0.1);
}

.preview-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 8px;
}

.remove-photo {
  position: absolute;
  top: 5px;
  right: 5px;
  width: 24px;
  height: 24px;
  background: rgba(255, 68, 68, 0.9);
  color: white;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.8rem;
  transition: all 0.2s;
}

.remove-photo:hover {
  background: #ff4444;
  transform: scale(1.1);
}

.add-more {
  aspect-ratio: 1;
  border: 2px dashed #e0e0e0;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: #666;
  transition: all 0.3s;
}

.add-more:hover {
  border-color: #f7871f;
  color: #f7871f;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 1px solid #e0e0e0;
}

.cancel-btn, .submit-btn {
  padding: 0.8rem 2rem;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
}

.cancel-btn {
  background: #f5f5f5;
  color: #666;
  border: none;
}

.submit-btn {
  background: #f7871f;
  color: white;
  border: none;
}

.cancel-btn:hover {
  background: #e0e0e0;
}

.submit-btn:hover {
  background: #e99a08;
}

.submit-btn:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.hidden {
  display: none;
}

.error-message {
  color: #ff4444;
  font-size: 0.85rem;
  margin-top: 0.5rem;
}

.photo-info-row {
  display: flex;
  gap: 2rem;
  margin-bottom: 0;
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

@media (max-width: 768px) {
  .admin-sidebar {
    width: 70px;
  }

  .sidebar-header {
    justify-content: center;
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

  .add-pet-container {
    padding: 1rem;
  }

  .pet-form {
    padding: 1.5rem;
  }

  .form-grid {
    grid-template-columns: 1fr;
  }

  .form-row {
    grid-template-columns: 1fr;
  }
}
</style>