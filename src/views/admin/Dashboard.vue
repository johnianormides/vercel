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
      <header class="admin-header">
        <div class="header-left">
          <h1>Dashboard</h1>
        </div>
        <div class="header-right">
          <div class="admin-profile">
            <img src="/Designer.png" alt="Admin" class="admin-avatar" />
            <span class="admin-name">Admin</span>
          </div>
        </div>
      </header>

      <div class="admin-content">
        <!-- Stats Cards -->
        <div class="stats-grid">
          <div class="stat-card">
            <div class="stat-icon">
              <i class="fas fa-paw"></i>
            </div>
            <div class="stat-info">
              <h3>Total Pets</h3>
              <p>{{ stats.totalPets }}</p>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon">
              <i class="fas fa-home"></i>
            </div>
            <div class="stat-info">
              <h3>Available for Adoption</h3>
              <p>{{ stats.availablePets }}</p>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon">
              <i class="fas fa-file-alt"></i>
            </div>
            <div class="stat-info">
              <h3>Pending Applications</h3>
              <p>{{ stats.pendingApplications }}</p>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon">
              <i class="fas fa-check-circle"></i>
            </div>
            <div class="stat-info">
              <h3>Completed Adoptions</h3>
              <p>{{ stats.completedAdoptions }}</p>
            </div>
          </div>
        </div>

        <!-- Charts Section -->
        <div class="charts-grid">
          <div class="chart-card">
            <h3>Monthly Adoptions</h3>
            <div class="chart-container">
              <canvas ref="adoptionsChart"></canvas>
            </div>
          </div>
          <div class="chart-card">
            <h3>Pet Categories</h3>
            <div class="chart-container">
              <canvas ref="categoriesChart"></canvas>
            </div>
          </div>
        </div>

        <!-- Recent Activity -->
        <div class="recent-activity">
          <h3>Recent Activity</h3>
          <div class="activity-list">
            <div v-for="activity in recentActivities" :key="activity.id" class="activity-item">
              <div class="activity-icon" :class="activity.type">
                <i :class="activity.icon"></i>
              </div>
              <div class="activity-details">
                <p class="activity-text">{{ activity.text }}</p>
                <span class="activity-time">{{ activity.time }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import Chart from 'chart.js/auto'

export default {
  name: 'AdminDashboard',
  data() {
    return {
      stats: {
        totalPets: 0,
        availablePets: 0,
        pendingApplications: 0,
        completedAdoptions: 0
      },
      petCategories: {
        dogs: 0,
        cats: 0
      },
      recentActivities: [
        {
          id: 1,
          type: 'adoption',
          icon: 'fas fa-home',
          text: 'New adoption request for Max (Labrador)',
          time: '2 hours ago'
        },
        {
          id: 2,
          type: 'pet',
          icon: 'fas fa-paw',
          text: 'New pet added: Luna (Persian Cat)',
          time: '4 hours ago'
        },
        {
          id: 3,
          type: 'application',
          icon: 'fas fa-file-alt',
          text: 'Application approved for Bella (Golden Retriever)',
          time: '1 day ago'
        }
      ]
    }
  },
  mounted() {
    this.fetchStats()
    this.fetchPetCategories()
      .then(() => {
    this.initCharts()
      })
  },
  methods: {
    handleLogout() {
      // Clear auth data from localStorage
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      // Redirect to login
      this.$router.push('/admin-login')
    },

    async fetchStats() {
      try {
        const statsResponse = await fetch('http://localhost:5000/api/admin/stats')
        const activitiesResponse = await fetch('http://localhost:5000/api/admin/recent-activities')

        if (!statsResponse.ok || !activitiesResponse.ok) {
          throw new Error('Failed to fetch dashboard data')
        }

        const statsData = await statsResponse.json()
        const activitiesData = await activitiesResponse.json()

        if (statsData.success) {
          this.stats = statsData.data
        }

        if (activitiesData.success) {
          this.recentActivities = activitiesData.data
        }
      } catch (error) {
        console.error('Error fetching dashboard data:', error)
        // Fallback to sample data if the API fails
        this.stats = {
          totalPets: 24,
          availablePets: 15,
          pendingApplications: 8,
          completedAdoptions: 12
        }
      }
    },

    async fetchPetCategories() {
      try {
        // Fetch all pets to calculate categories
        const response = await fetch('http://localhost:5000/api/pet')

        if (!response.ok) {
          throw new Error('Failed to fetch pets data')
        }

        const result = await response.json()

        if (result.success && result.data) {
          // Reset counters
          this.petCategories = {
            dogs: 0,
            cats: 0
          }

          // Count pets by species/type
          result.data.forEach(pet => {
            const species = pet.species ? pet.species.toLowerCase() : '';

            if (species === 'dog') {
              this.petCategories.dogs++;
            } else if (species === 'cat') {
              this.petCategories.cats++;
            }
          });
        }
      } catch (error) {
        console.error('Error fetching pet categories:', error)
        // Fallback to sample data
        this.petCategories = {
          dogs: 12,
          cats: 8
        }
      }
    },

    initCharts() {
      // Monthly Adoptions Chart
      const adoptionsCtx = this.$refs.adoptionsChart.getContext('2d')
      new Chart(adoptionsCtx, {
        type: 'line',
        data: {
          labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
          datasets: [{
            label: 'Adoptions',
            data: [0, 0, 2, 3, 2, 1],
            borderColor: '#f7871f',
            tension: 0.4,
            fill: false
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              display: false
            },
            title: {
              display: false
            }
          },
          scales: {
            y: {
              beginAtZero: true,
              ticks: {
                font: {
                  size: 9
                },
                maxTicksLimit: 4
              },
              grid: {
                display: false
              }
            },
            x: {
              ticks: {
                font: {
                  size: 9
                }
              },
              grid: {
                display: false
              }
            }
          },
          layout: {
            padding: {
              left: 2,
              right: 2,
              top: 2,
              bottom: 2
            }
          }
        }
      })

      // Pet Categories Chart
      const categoriesCtx = this.$refs.categoriesChart.getContext('2d')
      new Chart(categoriesCtx, {
        type: 'doughnut',
        data: {
          labels: ['Dogs', 'Cats'],
          datasets: [{
            data: [
              this.petCategories.dogs,
              this.petCategories.cats
            ],
            backgroundColor: ['#f7871f', '#4CAF50']
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          cutout: '60%',
          plugins: {
            legend: {
              position: 'bottom',
              labels: {
                boxWidth: 10,
                padding: 5,
                font: {
                  size: 9
                }
              }
            }
          },
          layout: {
            padding: {
              left: 2,
              right: 2,
              top: 2,
              bottom: 2
            }
          }
        }
      })
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

.admin-content {
  padding: 1rem;
  display: grid;
  grid-template-rows: auto auto;
  grid-template-columns: 3fr 2fr;
  grid-template-areas:
    "stats stats"
    "charts activity";
  gap: 0.75rem;
  overflow-y: auto;
}

.stats-grid {
  grid-area: stats;
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
}

.charts-grid {
  grid-area: charts;
  display: grid;
  grid-template-rows: auto auto;
  gap: 1rem;
}

.chart-card {
  background: #fff;
  border-radius: 12px;
  padding: 0.75rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
  display: flex;
  flex-direction: column;
  height: 180px; /* Smaller height */
}

.chart-card h3 {
  color: #222;
  font-size: 0.85rem;
  font-weight: 600;
  margin-bottom: 0.3rem;
}

.chart-container {
  flex: 1;
  min-height: 0; /* Important for chart sizing */
}

.recent-activity {
  grid-area: activity;
  background: #fff;
  border-radius: 12px;
  padding: 0.75rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
  height: 370px; /* Smaller height */
  display: flex;
  flex-direction: column;
}

.recent-activity h3 {
  color: #222;
  font-size: 0.9rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.activity-list {
  overflow-y: auto;
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  padding-right: 0.5rem;
}

/* Custom scrollbar for activity list */
.activity-list::-webkit-scrollbar {
  width: 6px;
}

.activity-list::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.activity-list::-webkit-scrollbar-thumb {
  background: #ddd;
  border-radius: 3px;
}

.activity-list::-webkit-scrollbar-thumb:hover {
  background: #ccc;
}

.activity-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem;
  border-radius: 8px;
  background: #f8f9fa;
  margin-bottom: 0.5rem;
}

.activity-icon {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1rem;
}

.activity-icon.adoption {
  background: #e3f2fd;
  color: #2196F3;
}

.activity-icon.pet {
  background: #fff5eb;
  color: #f7871f;
}

.activity-icon.application {
  background: #e8f5e9;
  color: #4CAF50;
}

.activity-details {
  flex: 1;
}

.activity-text {
  color: #333;
  font-size: 0.85rem;
  margin-bottom: 0.1rem;
}

.activity-time {
  color: #888;
  font-size: 0.75rem;
}

.stat-card {
  background: #fff;
  border-radius: 12px;
  padding: 1rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

.stat-icon {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  background: #fff5eb;
  color: #f7871f;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
}

.stat-info h3 {
  color: #666;
  font-size: 0.8rem;
  font-weight: 500;
  margin-bottom: 0.2rem;
}

.stat-info p {
  color: #222;
  font-size: 1.5rem;
  font-weight: 700;
}

/* Responsive Design */
@media (max-width: 1200px) {
  .admin-content {
    grid-template-columns: 1fr;
    grid-template-areas:
      "stats"
      "charts"
      "activity";
  }

  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .recent-activity {
    height: 350px;
  }

  .chart-card {
    height: 160px;
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

  .stats-grid {
    grid-template-columns: 1fr;
  }

  .recent-activity {
    height: 350px;
  }
}
</style>