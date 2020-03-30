<template>
  <div id="admin" class="admin">
    <el-container>
      <el-header>
        <el-menu
          :default-active="activeIndex"
          class="el-menu-demo"
          mode="horizontal"
          background-color="#545c64"
          text-color="#fff"
          active-text-color="#ffd04b"
        >
          <el-menu-item index="1">管理中心</el-menu-item>
          <el-menu-item index="2" style="float: right" @click="exit">退出</el-menu-item>
        </el-menu>
      </el-header>
      <el-container>
        <el-aside width="280px">
          <el-menu
            :default-active="active"
            class="el-menu-vertical-demo"
            background-color="#545c64"
            text-color="#fff"
            active-text-color="#ffd04b"
            router
          >
            <el-menu-item index="/admin/userinfo">
              <i class="el-icon-warning"></i>
              <span slot="title">我的信息</span>
            </el-menu-item>
            <el-menu-item index="/admin/department" v-if="jurisdictions.indexOf('1') > -1">
              <i class="el-icon-s-cooperation"></i>
              <span slot="title">分组管理</span>
            </el-menu-item>
            <el-menu-item index="/admin/jurisdiction" v-if="jurisdictions.indexOf('2') > -1">
              <i class="el-icon-s-help"></i>
              <span slot="title">权限管理</span>
            </el-menu-item>
            <el-menu-item index="/admin/user" v-if="jurisdictions.indexOf('3') > -1">
              <i class="el-icon-user-solid"></i>
              <span slot="title">用户管理</span>
            </el-menu-item>
          </el-menu>
        </el-aside>
        <el-main>
          <router-view />
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
export default {
  name: 'admin',
  data() {
    return {
      activeIndex: '1',
      active: '/admin/userinfo',
      jurisdictions: []
    }
  },
  methods: {
    exit() {
      localStorage.clear()
      this.$router.push('/auth')
    },
    get_jurisdictions() {
      this.axios
        .get(`${this.url}/auth/${this.$store.state.token}/`)
        .then(res => {
          if (res.data.code === 200) {
            this.jurisdictions = res.data.data
          } else {
            this.$message.error(res.data.msg)
          }
        })
        .catch(err => {
          this.$message.error(err)
        })
    }
  },
  mounted() {
    if (!this.$store.state.token) {
      localStorage.clear()
      this.$router.push('/auth')
      return
    }
    this.get_jurisdictions()
    this.active = this.$route.path
  },
  watch: {
    '$store.state.refresh': function(v1, v2) {
      this.get_jurisdictions()
    }
  }
}
</script>

<style lang="scss" scoped>
#admin {
  width: 100%;
  height: 100%;
  overflow: hidden;
  .el-container {
    height: 100%;
  }

  .el-header {
    padding: 0;
  }

  .el-aside {
    padding: 0;
    .el-menu {
      height: 100%;
      border-right: none;
    }
  }

  .el-main {
    padding: 0;
  }
}
</style>
