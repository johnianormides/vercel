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
        <router-link to="/admin/pets" class="nav-item" active-class="active">
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
      <div class="applications">
        <div class="page-header">
          <div class="header-content">
            <h2>Adoption Applications</h2>
            <p class="subtitle">Review and manage adoption applications</p>
          </div>
          <div class="header-actions">
            <button class="refresh-btn" @click="fetchApplications" title="Refresh Applications">
              <i class="fas fa-sync-alt"></i>
              Refresh
            </button>
          </div>
        </div>

        <!-- Stats Cards -->
        <div class="stats-row">
          <div class="stat-card">
            <div class="stat-icon">
              <i class="fas fa-file-alt"></i>
            </div>
            <div class="stat-info">
              <p class="stat-value">{{ applications.length }}</p>
              <p class="stat-label">Total Applications</p>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon pending">
              <i class="fas fa-clock"></i>
            </div>
            <div class="stat-info">
              <p class="stat-value">{{ pendingApplications.length }}</p>
              <p class="stat-label">Pending</p>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon approved">
              <i class="fas fa-check-circle"></i>
            </div>
            <div class="stat-info">
              <p class="stat-value">{{ approvedApplications.length }}</p>
              <p class="stat-label">Approved</p>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon rejected">
              <i class="fas fa-times-circle"></i>
            </div>
            <div class="stat-info">
              <p class="stat-value">{{ rejectedApplications.length }}</p>
              <p class="stat-label">Rejected</p>
            </div>
          </div>
        </div>

        <!-- Filters -->
        <div class="filter-section">
          <div class="search-box">
            <i class="fas fa-search"></i>
            <input
              type="text"
              v-model="searchQuery"
              placeholder="Search by applicant name, pet name, or status..."
              @input="filterApplications"
            />
          </div>
          <div class="filter-options">
            <div class="filter-item">
              <label>Time Period</label>
              <select v-model="dateFilter" @change="filterApplications">
                <option value="">All Time</option>
                <option value="today">Today</option>
                <option value="week">This Week</option>
                <option value="month">This Month</option>
              </select>
            </div>
          </div>
        </div>

        <!-- Applications Tables -->
        <div class="applications-container">
          <!-- Pending Applications -->
          <div class="application-section">
            <div class="section-header pending">
              <div class="section-title">
                <i class="fas fa-clock"></i>
                <h3>Pending Applications</h3>
              </div>
              <span class="count-badge">{{ pendingApplications.length }}</span>
            </div>
            <div class="table-container">
              <table class="applications-table">
                <thead>
                  <tr>
                    <th class="th-applicant">Applicant</th>
                    <th class="th-pet">Pet</th>
                    <th class="th-date">Applied Date</th>
                    <th class="th-actions">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-if="pendingApplications.length === 0">
                    <td colspan="4" class="no-data">
                      <div class="no-data-content">
                        <i class="fas fa-inbox"></i>
                        <p>No pending applications</p>
                      </div>
                    </td>
                  </tr>
                  <tr v-for="application in pendingApplications" :key="application.id" class="application-row">
                    <td>
                      <div class="applicant-info">
                        <img :src="application.applicant.avatar" :alt="application.applicant.name" class="applicant-avatar" />
                        <div>
                          <p class="applicant-name">{{ application.applicant.name }}</p>
                          <p class="applicant-email">{{ application.applicant.email }}</p>
                        </div>
                      </div>
                    </td>
                    <td>
                      <div class="pet-info">
                        <img :src="application.pet.photo" :alt="application.pet.name" class="pet-photo" />
                        <div>
                          <p class="pet-name">{{ application.pet.name }}</p>
                          <p class="pet-breed">{{ application.pet.breed }}</p>
                        </div>
                      </div>
                    </td>
                    <td>
                      <div class="date-info">
                        <p class="date-value">{{ formatDate(application.appliedDate) }}</p>
                        <p class="date-time">{{ formatTime(application.appliedDate) }}</p>
                      </div>
                    </td>
                    <td>
                      <div class="action-buttons">
                        <button class="action-btn view" @click="viewApplication(application)" title="View Details">
                          <i class="fas fa-eye"></i>
                        </button>
                        <button class="action-btn approve" @click="updateStatus(application, 'Approved')" title="Approve Application">
                          <i class="fas fa-check"></i>
                        </button>
                        <button class="action-btn reject" @click="updateStatus(application, 'Rejected')" title="Reject Application">
                          <i class="fas fa-times"></i>
                        </button>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- Approved Applications -->
          <div class="application-section">
            <div class="section-header approved">
              <div class="section-title">
                <i class="fas fa-check-circle"></i>
                <h3>Approved Applications</h3>
              </div>
              <span class="count-badge">{{ approvedApplications.length }}</span>
            </div>
            <div class="table-container">
              <table class="applications-table">
                <thead>
                  <tr>
                    <th class="th-applicant">Applicant</th>
                    <th class="th-pet">Pet</th>
                    <th class="th-date">Approved Date</th>
                    <th class="th-actions">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-if="approvedApplications.length === 0">
                    <td colspan="4" class="no-data">
                      <div class="no-data-content">
                        <i class="fas fa-check-circle"></i>
                        <p>No approved applications</p>
                      </div>
                    </td>
                  </tr>
                  <tr v-for="application in approvedApplications" :key="application.id" class="application-row">
                    <td>
                      <div class="applicant-info">
                        <img :src="application.applicant.avatar" :alt="application.applicant.name" class="applicant-avatar" />
                        <div>
                          <p class="applicant-name">{{ application.applicant.name }}</p>
                          <p class="applicant-email">{{ application.applicant.email }}</p>
                        </div>
                      </div>
                    </td>
                    <td>
                      <div class="pet-info">
                        <img :src="application.pet.photo" :alt="application.pet.name" class="pet-photo" />
                        <div>
                          <p class="pet-name">{{ application.pet.name }}</p>
                          <p class="pet-breed">{{ application.pet.breed }}</p>
                        </div>
                      </div>
                    </td>
                    <td>
                      <div class="date-info">
                        <p class="date-value">{{ formatDate(application.appliedDate) }}</p>
                        <p class="date-time">{{ formatTime(application.appliedDate) }}</p>
                      </div>
                    </td>
                    <td>
                      <div class="action-buttons">
                        <button class="action-btn view" @click="viewApplication(application)" title="View Details">
                          <i class="fas fa-eye"></i>
                        </button>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- Rejected Applications -->
          <div class="application-section">
            <div class="section-header rejected">
              <div class="section-title">
                <i class="fas fa-times-circle"></i>
                <h3>Rejected Applications</h3>
              </div>
              <span class="count-badge">{{ rejectedApplications.length }}</span>
            </div>
            <div class="table-container">
              <table class="applications-table">
                <thead>
                  <tr>
                    <th class="th-applicant">Applicant</th>
                    <th class="th-pet">Pet</th>
                    <th class="th-date">Rejected Date</th>
                    <th class="th-actions">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-if="rejectedApplications.length === 0">
                    <td colspan="4" class="no-data">
                      <div class="no-data-content">
                        <i class="fas fa-times-circle"></i>
                        <p>No rejected applications</p>
                      </div>
                    </td>
                  </tr>
                  <tr v-for="application in rejectedApplications" :key="application.id" class="application-row">
                    <td>
                      <div class="applicant-info">
                        <img :src="application.applicant.avatar" :alt="application.applicant.name" class="applicant-avatar" />
                        <div>
                          <p class="applicant-name">{{ application.applicant.name }}</p>
                          <p class="applicant-email">{{ application.applicant.email }}</p>
                        </div>
                      </div>
                    </td>
                    <td>
                      <div class="pet-info">
                        <img :src="application.pet.photo" :alt="application.pet.name" class="pet-photo" />
                        <div>
                          <p class="pet-name">{{ application.pet.name }}</p>
                          <p class="pet-breed">{{ application.pet.breed }}</p>
                        </div>
                      </div>
                    </td>
                    <td>
                      <div class="date-info">
                        <p class="date-value">{{ formatDate(application.appliedDate) }}</p>
                        <p class="date-time">{{ formatTime(application.appliedDate) }}</p>
                      </div>
                    </td>
                    <td>
                      <div class="action-buttons">
                        <button class="action-btn view" @click="viewApplication(application)" title="View Details">
                          <i class="fas fa-eye"></i>
                        </button>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <!-- View Application Modal -->
        <div v-if="showViewModal" class="modal-overlay" @click.self="showViewModal = false">
          <div class="modal">
            <div class="modal-header">
              <h3>Application Details</h3>
              <button class="close-btn" @click="showViewModal = false">&times;</button>
            </div>
            <div class="modal-content" v-if="selectedApplication">
              <div class="application-summary">
                <div class="application-status">
                  <span class="status-badge large" :class="selectedApplication.status.toLowerCase()">
                    {{ selectedApplication.status }}
                  </span>
                  <p class="application-id">Application ID: #{{ selectedApplication.id }}</p>
                </div>
                <div class="application-date">
                  <i class="fas fa-calendar-alt"></i>
                  <span>Applied on {{ formatDate(selectedApplication.appliedDate) }}</span>
                </div>
              </div>

              <div class="detail-section">
                <h4><i class="fas fa-user"></i> Applicant Information</h4>
                <div class="detail-grid">
                  <div class="detail-item">
                    <label>Name</label>
                    <p>{{ selectedApplication.applicant.name }}</p>
                  </div>
                  <div class="detail-item">
                    <label>Email</label>
                    <p>{{ selectedApplication.applicant.email }}</p>
                  </div>
                  <div class="detail-item">
                    <label>Age</label>
                    <p>{{ selectedApplication.applicantDetails?.age || 'Not provided' }}</p>
                  </div>
                  <div class="detail-item">
                    <label>Phone (Work)</label>
                    <p>{{ selectedApplication.applicantDetails?.workPhone || 'Not provided' }}</p>
                  </div>
                </div>
              </div>

              <div class="detail-section">
                <h4><i class="fas fa-home"></i> Living Situation</h4>
                <div class="detail-grid">
                  <div class="detail-item">
                    <label>Home Type</label>
                    <p>{{ selectedApplication.livingSituation?.homeType || 'Not provided' }}</p>
                  </div>
                  <div class="detail-item">
                    <label>Pets Allowed</label>
                    <p v-if="selectedApplication.livingSituation?.homeType === 'Condo/Townhome/Apartment'">
                      {{ selectedApplication.livingSituation?.petsAllowed ? 'Yes' : 'No' }}
                    </p>
                    <p v-else>Not applicable</p>
                  </div>
                  <div class="detail-item full-width">
                    <label>Address</label>
                    <p>
                      {{ selectedApplication.livingSituation?.address?.street || 'Not provided' }}<br>
                      {{ selectedApplication.livingSituation?.address?.city || '' }}
                      {{ selectedApplication.livingSituation?.address?.state || '' }}
                      {{ selectedApplication.livingSituation?.address?.zip || '' }}<br>
                      {{ selectedApplication.livingSituation?.address?.country || '' }}
                    </p>
                  </div>
                </div>
              </div>

              <div class="detail-section">
                <h4><i class="fas fa-paw"></i> Pet Information</h4>
                <div class="pet-summary">
                  <img :src="selectedApplication.pet.photo" :alt="selectedApplication.pet.name" class="pet-detail-photo" />
                  <div class="pet-details">
                    <div class="detail-grid">
                      <div class="detail-item">
                        <label>Name</label>
                        <p>{{ selectedApplication.pet.name }}</p>
                      </div>
                      <div class="detail-item">
                        <label>Breed</label>
                        <p>{{ selectedApplication.pet.breed }}</p>
                      </div>
                      <div class="detail-item">
                        <label>Age</label>
                        <p>{{ selectedApplication.pet.age }}</p>
                      </div>
                      <div class="detail-item">
                        <label>Gender</label>
                        <p>{{ selectedApplication.pet.gender }}</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <div class="detail-section">
                <h4><i class="fas fa-paw"></i> Other Pets</h4>
                <div class="detail-grid">
                  <div class="detail-item">
                    <label>Has Other Pets</label>
                    <p>{{ selectedApplication.otherPets?.hasPets ? 'Yes' : 'No' }}</p>
                  </div>
                  <div class="detail-item" v-if="selectedApplication.otherPets?.hasPets">
                    <label>Used to Other Pets</label>
                    <p>{{ selectedApplication.otherPets?.usedToOthers ? 'Yes' : 'No' }}</p>
                  </div>
                </div>
              </div>

              <div class="detail-section">
                <h4><i class="fas fa-clipboard-list"></i> Financial Readiness</h4>
                <div class="detail-grid">
                  <div class="detail-item">
                    <label>Ready for Financial Needs</label>
                    <p>{{ selectedApplication.experience?.financialReadiness ? 'Yes' : 'No' }}</p>
                  </div>
                </div>
              </div>

              <div class="detail-section">
                <h4><i class="fas fa-clipboard-list"></i> Application Reason</h4>
                <div class="detail-grid">
                  <div class="detail-item full-width">
                    <label>Reason for Adoption</label>
                    <p class="text-area">{{ selectedApplication.reason || 'No reason provided' }}</p>
                  </div>
                </div>
              </div>

              <!-- Uploaded Files Section -->
              <div class="detail-section">
                <h4><i class="fas fa-file-alt"></i> Uploaded Documents</h4>
                <div class="documents-grid">
                  <div class="document-item">
                    <label>Valid ID</label>
                    <div class="document-preview">
                      <div v-if="selectedApplication.validIdUrl" class="document-container">
                        <img :src="selectedApplication.validIdUrl" alt="Valid ID" class="document-image" />
                        <a :href="selectedApplication.validIdUrl" target="_blank" class="view-document-btn">
                          <i class="fas fa-external-link-alt"></i> View Full Size
                        </a>
                      </div>
                      <div v-else class="no-document">
                        <i class="fas fa-file-image"></i>
                        <p>No ID document uploaded</p>
                      </div>
                    </div>
                  </div>
                  <div class="document-item">
                    <label>House Image</label>
                    <div class="document-preview">
                      <div v-if="selectedApplication.houseImageUrl" class="document-container">
                        <img :src="selectedApplication.houseImageUrl" alt="House Image" class="document-image" />
                        <a :href="selectedApplication.houseImageUrl" target="_blank" class="view-document-btn">
                          <i class="fas fa-external-link-alt"></i> View Full Size
                        </a>
                      </div>
                      <div v-else class="no-document">
                        <i class="fas fa-file-image"></i>
                        <p>No house image uploaded</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <div class="modal-actions" v-if="selectedApplication.status === 'Pending'">
                <button class="approve-btn" @click="updateStatus(selectedApplication, 'Approved')">
                  <i class="fas fa-check"></i>
                  Approve Application
                </button>
                <button class="reject-btn" @click="updateStatus(selectedApplication, 'Rejected')">
                  <i class="fas fa-times"></i>
                  Reject Application
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
export default {
  name: 'AdminApplications',
  data() {
    return {
      applications: [],
      searchQuery: '',
      statusFilter: '',
      dateFilter: '',
      showViewModal: false,
      selectedApplication: null,
      loading: false,
      error: null
    }
  },
  computed: {
    filteredApplications() {
      return this.applications.filter(app => {
        const matchesSearch =
          app.applicant.name.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
          app.pet.name.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
          app.status.toLowerCase().includes(this.searchQuery.toLowerCase())

        const matchesStatus = !this.statusFilter || app.status === this.statusFilter
        const matchesDate = this.filterByDate(app.appliedDate)

        return matchesSearch && matchesStatus && matchesDate
      })
    },
    pendingApplications() {
      return this.applications.filter(app => app.status === 'Pending')
    },
    approvedApplications() {
      return this.applications.filter(app => app.status === 'Approved')
    },
    rejectedApplications() {
      return this.applications.filter(app => app.status === 'Rejected')
    }
  },
  mounted() {
    this.fetchApplications()
  },
  methods: {
    async fetchApplications() {
      this.loading = true
      this.error = null
      try {
        const response = await fetch('http://localhost:5000/api/application')
        if (!response.ok) {
          throw new Error('Failed to fetch applications')
        }

        const result = await response.json()
        console.log('Raw applications data:', result.data) // Debug log

        if (result.success && result.data) {
          // Format the data from our Flask/Supabase backend to match the component's expectations
          this.applications = await Promise.all(result.data.map(async app => {
            // Fetch user details
            const userResponse = await fetch(`http://localhost:5000/api/user/${app.user_id}`)
            const userData = await userResponse.json()
            const user = userData.success ? userData.data : { name: 'Unknown', email: 'unknown@example.com' }

            // Fetch pet details
            const petResponse = await fetch(`http://localhost:5000/api/pet/${app.pet_id}`)
            const petData = await petResponse.json()
            const pet = petData.success ? petData.data : { name: 'Unknown Pet', breed: 'Unknown' }

            // Parse JSON fields from application
            let livingSituation = {}
            let otherPets = {}
            let experience = {}

            try {
              // Parse living_situation
              if (typeof app.living_situation === 'string') {
                livingSituation = JSON.parse(app.living_situation)
              } else if (typeof app.living_situation === 'object') {
                livingSituation = app.living_situation
              }

              // Parse other_pets
              if (typeof app.other_pets === 'string') {
                otherPets = JSON.parse(app.other_pets)
              } else if (typeof app.other_pets === 'object') {
                otherPets = app.other_pets
              }

              // Parse experience
              if (typeof app.experience === 'string') {
                experience = JSON.parse(app.experience)
              } else if (typeof app.experience === 'object') {
                experience = app.experience
              }

              console.log('Application ID:', app.id)
              console.log('Parsed living_situation:', livingSituation)
              console.log('Parsed other_pets:', otherPets)
              console.log('Parsed experience:', experience)
            } catch (e) {
              console.error('Error parsing application JSON fields:', e)
            }

            // Get the file URLs from living_situation
            const validIdUrl = livingSituation.documents?.valid_id_url || null
            const houseImageUrl = livingSituation.documents?.house_image_url || null

            // Extract applicant details from experience
            const contactInfo = experience.contact_info || {}

            return {
              id: app.id,
              user_id: app.user_id,
              pet_id: app.pet_id,
              applicant: {
                name: user.name,
                email: user.email,
                avatar: user.profile_image || 'https://via.placeholder.com/40'
              },
              applicantDetails: {
                age: app.age || '',
                workPhone: contactInfo.work_phone || ''
              },
              pet: {
                name: pet.name,
                breed: pet.breed,
                age: pet.age ? `${pet.age} years` : 'Unknown',
                gender: pet.gender || 'Unknown',
                photo: pet.image_url || pet.photo_url || 'https://via.placeholder.com/40'
              },
              appliedDate: app.application_date,
              status: app.status.charAt(0).toUpperCase() + app.status.slice(1),
              reason: app.reason,
              livingSituation: {
                homeType: livingSituation.home_type || '',
                petsAllowed: livingSituation.pets_allowed === 'Yes',
                address: livingSituation.address || {}
              },
              otherPets: {
                hasPets: otherPets.has_pets || false,
                usedToOthers: otherPets.used_to_others || false
              },
              experience: {
                contactInfo: contactInfo,
                financialReadiness: experience.financial_readiness || false
              },
              validIdUrl: validIdUrl,
              houseImageUrl: houseImageUrl
            }
          }))

          console.log('Processed applications:', this.applications) // Debug log
        } else {
          throw new Error(result.message || 'Failed to fetch applications')
        }
      } catch (error) {
        console.error('Error fetching applications:', error)
        this.error = 'Failed to load applications. Please try again.'
      } finally {
        this.loading = false
      }
    },
    filterApplications() {
      // Filtering is handled by computed property
    },
    filterByDate(date) {
      if (!this.dateFilter) return true

      const applicationDate = new Date(date)
      const today = new Date()
      const startOfWeek = new Date(today.setDate(today.getDate() - today.getDay()))
      const startOfMonth = new Date(today.getFullYear(), today.getMonth(), 1)

      switch (this.dateFilter) {
        case 'today':
          return applicationDate.toDateString() === new Date().toDateString()
        case 'week':
          return applicationDate >= startOfWeek
        case 'month':
          return applicationDate >= startOfMonth
        default:
          return true
      }
    },
    formatDate(date) {
      if (!date) return 'N/A'
      return new Date(date).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      })
    },
    formatTime(date) {
      if (!date) return 'N/A'
      return new Date(date).toLocaleTimeString('en-US', {
        hour: 'numeric',
        minute: '2-digit'
      })
    },
    viewApplication(application) {
      this.selectedApplication = application
      this.showViewModal = true
    },
    async updateStatus(application, newStatus) {
      try {
        const response = await fetch(`http://localhost:5000/api/application/${application.id}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            status: newStatus.toLowerCase(),
            admin_notes: `Status updated to ${newStatus} on ${new Date().toISOString()}`
          })
        })

        if (!response.ok) {
          throw new Error('Failed to update application status')
        }

        const result = await response.json()

        if (result.success) {
        // Update local state
        application.status = newStatus
        if (this.selectedApplication?.id === application.id) {
          this.selectedApplication.status = newStatus
        }
        this.showViewModal = false
        } else {
          throw new Error(result.message || 'Failed to update application status')
        }
      } catch (error) {
        console.error('Error updating application status:', error)
        alert('Failed to update application status. Please try again.')
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
  padding: 1.5rem;
}

.applications {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  height: calc(100vh - 100px);
  overflow-y: auto;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.header-content {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.header-content h2 {
  color: #222;
  font-size: 1.75rem;
  font-weight: 600;
  margin: 0;
}

.header-content p.subtitle {
  color: #666;
  font-size: 0.95rem;
  margin: 0;
}

.header-actions {
  display: flex;
  gap: 1rem;
}

.refresh-btn {
  background: #f4f6fa;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  color: #2196F3;
  font-size: 0.9rem;
  padding: 0.6rem 1rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.2s ease;
}

.refresh-btn:hover {
  background: #e3f2fd;
  border-color: #bbdefb;
  transform: translateY(-2px);
}

/* Stats Row */
.stats-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.stat-card {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
  padding: 1.25rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 5px 15px rgba(0,0,0,0.08);
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  background: #f0f4f8;
  color: #5c7cfa;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.4rem;
}

.stat-icon.pending {
  background: #fff3e0;
  color: #ff9800;
}

.stat-icon.approved {
  background: #e8f5e9;
  color: #4CAF50;
}

.stat-icon.rejected {
  background: #ffebee;
  color: #f44336;
}

.stat-info {
  display: flex;
  flex-direction: column;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: 600;
  color: #333;
  margin: 0;
  line-height: 1.2;
}

.stat-label {
  color: #666;
  font-size: 0.85rem;
  margin: 0;
}

/* Filter Section */
.filter-section {
  background: #fff;
  border-radius: 12px;
  padding: 1.25rem;
  display: flex;
  gap: 1.5rem;
  align-items: flex-end;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
  margin-bottom: 1.5rem;
}

.search-box {
  flex: 1;
  position: relative;
}

.search-box i {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  color: #888;
}

.search-box input {
  width: 100%;
  padding: 0.75rem 1rem 0.75rem 2.75rem;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  font-size: 0.95rem;
  transition: all 0.2s;
}

.search-box input:focus {
  border-color: #5c7cfa;
  box-shadow: 0 0 0 3px rgba(92, 124, 250, 0.15);
  outline: none;
}

.filter-options {
  display: flex;
  gap: 1rem;
}

.filter-item {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.filter-item label {
  font-size: 0.85rem;
  color: #666;
  font-weight: 500;
}

.filter-item select {
  padding: 0.75rem 1rem;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  font-size: 0.95rem;
  min-width: 150px;
  background-color: #fff;
  transition: all 0.2s;
}

.filter-item select:focus {
  border-color: #5c7cfa;
  box-shadow: 0 0 0 3px rgba(92, 124, 250, 0.15);
  outline: none;
}

/* Applications Container */
.applications-container {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  padding-bottom: 2rem;
}

.application-section {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.section-header {
  padding: 1.25rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #e0e0e0;
  background: #fff;
  position: sticky;
  top: 0;
  z-index: 10;
}

.section-header.pending {
  border-left: 4px solid #ff9800;
}

.section-header.approved {
  border-left: 4px solid #4CAF50;
}

.section-header.rejected {
  border-left: 4px solid #f44336;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.section-title i {
  font-size: 1.1rem;
}

.section-title i.fa-clock {
  color: #ff9800;
}

.section-title i.fa-check-circle {
  color: #4CAF50;
}

.section-title i.fa-times-circle {
  color: #f44336;
}

.section-title h3 {
  color: #222;
  font-size: 1.1rem;
  font-weight: 600;
  margin: 0;
}

.count-badge {
  padding: 0.4rem 0.8rem;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 500;
  background: #f8f9fa;
  color: #666;
}

.table-container {
  padding: 0;
  overflow-x: auto;
  max-height: 400px;
  overflow-y: auto;
}

/* Custom scrollbar for table container */
.table-container::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}

.table-container::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.table-container::-webkit-scrollbar-thumb {
  background: #ddd;
  border-radius: 3px;
}

.table-container::-webkit-scrollbar-thumb:hover {
  background: #ccc;
}

.applications-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
}

.applications-table th {
  background: #f8f9fa;
  font-weight: 600;
  color: #555;
  font-size: 0.9rem;
  padding: 1rem;
  text-align: left;
  position: sticky;
  top: 0;
  z-index: 5;
  border-bottom: 2px solid #e0e0e0;
}

.applications-table td {
  padding: 1rem;
  border-bottom: 1px solid #e0e0e0;
  vertical-align: middle;
}

.application-row {
  transition: all 0.2s;
}

.application-row:hover {
  background-color: #f8f9fa;
}

/* Column widths */
.th-applicant {
  width: 30%;
}

.th-pet {
  width: 30%;
}

.th-date {
  width: 20%;
}

.th-actions {
  width: 20%;
}

.applicant-info,
.pet-info {
  display: flex;
  align-items: center;
  gap: 0.8rem;
}

.applicant-avatar,
.pet-photo {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  object-fit: cover;
}

.applicant-name,
.pet-name {
  color: #222;
  font-weight: 500;
  margin-bottom: 0.2rem;
}

.applicant-email,
.pet-breed {
  color: #888;
  font-size: 0.85rem;
}

.date-info {
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
}

.date-value {
  color: #333;
  font-weight: 500;
  margin: 0;
}

.date-time {
  color: #888;
  font-size: 0.85rem;
  margin: 0;
}

.status-badge {
  padding: 0.4rem 0.8rem;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 500;
}

.status-badge.pending {
  background: #fff3e0;
  color: #ff9800;
}

.status-badge.approved {
  background: #e8f5e9;
  color: #4CAF50;
}

.status-badge.rejected {
  background: #ffebee;
  color: #f44336;
}

.status-badge.cancelled {
  background: #f5f5f5;
  color: #9e9e9e;
}

.action-buttons {
  display: flex;
  gap: 0.5rem;
}

.action-btn {
  width: 32px;
  height: 32px;
  border-radius: 6px;
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
}

.action-btn.view {
  background: #e3f2fd;
  color: #2196F3;
}

.action-btn.approve {
  background: #e8f5e9;
  color: #4CAF50;
}

.action-btn.reject {
  background: #ffebee;
  color: #f44336;
}

.action-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 3px 5px rgba(0, 0, 0, 0.1);
}

/* No data state */
.no-data {
  padding: 2rem;
  text-align: center;
}

.no-data-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
}

.no-data-content i {
  font-size: 2rem;
  color: #ccc;
}

.no-data-content p {
  color: #888;
  font-size: 0.95rem;
  margin: 0;
}

/* Modal styling */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0,0,0,0.4);
  backdrop-filter: blur(3px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal {
  background: #fff;
  border-radius: 12px;
  width: 90%;
  max-width: 800px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

/* Custom scrollbar for modal */
.modal::-webkit-scrollbar {
  width: 6px;
}

.modal::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.modal::-webkit-scrollbar-thumb {
  background: #ddd;
  border-radius: 3px;
}

.modal::-webkit-scrollbar-thumb:hover {
  background: #ccc;
}

.modal-header {
  padding: 1.5rem;
  border-bottom: 1px solid #e0e0e0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: sticky;
  top: 0;
  background: #fff;
  z-index: 10;
}

.modal-header h3 {
  color: #222;
  font-size: 1.2rem;
  font-weight: 600;
  margin: 0;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  color: #888;
  cursor: pointer;
  transition: all 0.2s;
}

.close-btn:hover {
  color: #333;
}

.modal-content {
  padding: 1.5rem;
}

.application-summary {
  margin-bottom: 1.5rem;
}

.application-status {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
}

.status-badge.large {
  padding: 0.4rem 0.8rem;
  border-radius: 20px;
  font-size: 1rem;
  font-weight: 500;
}

.application-id {
  color: #888;
  font-size: 0.85rem;
}

.application-date {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #888;
  font-size: 0.85rem;
}

.application-date i {
  font-size: 1rem;
}

.detail-section {
  margin-bottom: 1.5rem;
  background: #f8f9fa;
  border-radius: 12px;
  padding: 1.25rem;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
  border-left: 3px solid #e0e0e0;
  transition: all 0.2s ease;
}

.detail-section:hover {
  border-left-color: #f7871f;
  background: #fafbfc;
}

.detail-section h4 {
  color: #333;
  font-size: 1.1rem;
  font-weight: 600;
  margin: 0 0 1rem 0;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.detail-section h4 i {
  color: #f7871f;
  font-size: 1.2rem;
}

.detail-item {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.detail-item label {
  color: #666;
  font-size: 0.9rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.detail-item p {
  color: #333;
  font-size: 1rem;
  background: #fff;
  padding: 0.85rem;
  border-radius: 8px;
  margin: 0;
  border: 1px solid #eee;
  box-shadow: 0 1px 2px rgba(0,0,0,0.03);
}

.detail-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.detail-item.full-width {
  grid-column: 1 / -1;
}

.pet-summary {
  display: flex;
  align-items: center;
  gap: 0.8rem;
}

.pet-detail-photo {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  object-fit: cover;
}

.pet-details {
  flex: 1;
}

.text-area {
  padding: 0.75rem;
  border-radius: 6px;
  border: 1px solid #e0e0e0;
  background: #fff;
  margin: 0;
}

.documents-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
}

.document-item {
  flex: 1;
}

.document-preview {
  margin-top: 0.5rem;
}

.document-container {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  background: #fff;
  padding: 1rem;
  border-radius: 8px;
  border: 1px solid #e0e0e0;
}

.document-image {
  max-width: 100%;
  max-height: 300px;
  object-fit: contain;
  border-radius: 4px;
  border: 1px solid #e0e0e0;
}

.view-document-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  color: #2196F3;
  text-decoration: none;
  font-size: 0.9rem;
  padding: 0.5rem;
  border-radius: 4px;
  background: #e3f2fd;
  transition: all 0.3s ease;
}

.view-document-btn:hover {
  background: #bbdefb;
  text-decoration: none;
}

.no-document {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  background: #fff;
  border-radius: 8px;
  border: 1px dashed #e0e0e0;
  color: #888;
}

.no-document i {
  font-size: 2rem;
  margin-bottom: 0.5rem;
}

.no-document p {
  font-size: 0.9rem;
  margin: 0;
}

.modal-actions {
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
  padding-top: 1.5rem;
  border-top: 1px solid #e0e0e0;
}

.approve-btn,
.reject-btn {
  flex: 1;
  padding: 0.8rem;
  border-radius: 8px;
  font-weight: 500;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  cursor: pointer;
  transition: all 0.2s;
}

.approve-btn {
  background: #e8f5e9;
  color: #4CAF50;
  border: none;
}

.reject-btn {
  background: #ffebee;
  color: #f44336;
  border: none;
}

.approve-btn:hover {
  background: #c8e6c9;
  transform: translateY(-2px);
}

.reject-btn:hover {
  background: #ffcdd2;
  transform: translateY(-2px);
}

/* Custom scrollbar for main content */
.applications::-webkit-scrollbar {
  width: 8px;
}

.applications::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

.applications::-webkit-scrollbar-thumb {
  background: #ddd;
  border-radius: 4px;
}

.applications::-webkit-scrollbar-thumb:hover {
  background: #ccc;
}

/* Responsive Design */
@media (max-width: 1200px) {
  .stats-row {
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
  }
}

@media (max-width: 992px) {
  .filter-section {
    flex-direction: column;
    align-items: stretch;
    gap: 1rem;
  }

  .filter-options {
    width: 100%;
  }

  .filter-item {
    flex: 1;
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
    padding: 1rem;
  }

  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .applications {
    height: calc(100vh - 80px);
  }

  .stats-row {
    grid-template-columns: 1fr;
  }

  .table-container {
    max-height: 300px;
  }

  .filter-options {
    flex-direction: column;
  }

  .applications-table {
    display: block;
    overflow-x: auto;
  }

  .modal {
    width: 95%;
    margin: 1rem;
  }

  .documents-grid {
    grid-template-columns: 1fr;
  }
}
</style>