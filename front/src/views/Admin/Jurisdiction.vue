<template>
  <div
    id="jurisdiction"
    class="jurisdiction"
    v-loading="loading"
    element-loading-text="拼命加载中"
    element-loading-spinner="el-icon-loading"
    element-loading-background="rgba(0, 0, 0, 0.8)"
  >
    <div class="title">
      <h2>权限列表</h2>
      <el-button @click="dialogTitle = '添加权限';dialogManage = true">添 加</el-button>
    </div>
    <el-divider></el-divider>
    <el-table
      :data="jurisdictions.filter(data => !search || data.name.toLowerCase().includes(search.toLowerCase()))"
      style="width: 100%"
    >
      <el-table-column label="Name" prop="name"></el-table-column>
      <el-table-column label="Describe" prop="describe"></el-table-column>
      <el-table-column label="Identification" prop="identification"></el-table-column>
      <el-table-column align="right">
        <template slot="header" slot-scope="scope">
          <el-input v-model="search" size="mini" placeholder="输入关键字搜索" />
        </template>
        <template slot-scope="scope">
          <el-button size="mini" @click="handleEdit(scope.row)">Edit</el-button>
          <el-button size="mini" type="danger" @click="handleDelete(scope.row)">Delete</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-dialog :title="dialogTitle" :visible.sync="dialogManage" @close="close">
      <el-form :model="form" label-width="80px">
        <el-form-item label="权限名称">
          <el-input v-model="form.name" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="权限描述">
          <el-input v-model="form.describe" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="权限标识">
          <el-input v-model="form.identification" autocomplete="off"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogManage = false">取 消</el-button>
        <el-button type="primary" @click="handlerAdd">确 定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: 'jurisdiction',
  data() {
    return {
      jurisdictions: [],
      search: '',
      loading: false,
      dialogManage: false,
      dialogTitle: '添加权限',
      form: {}
    }
  },
  methods: {
    handlerAdd() {
      if (this.form.hasOwnProperty('id')) {
        this.loading = true
        this.axios
          .put(`${this.url}/jurisdiction/${this.form.id}/`, this.form)
          .then(res => {
            if (res.data.code === 200) {
              this.$message({
                message: '更新成功',
                type: 'success'
              })
              this.dialogManage = false
              this.get_jurisdictions()
            } else {
              this.$message.error(res.data.msg)
            }
            this.loading = false
          })
          .catch(err => {
            this.$message.error(err)
            this.loading = false
          })
      } else {
        this.loading = true
        this.axios
          .post(`${this.url}/jurisdiction/`, this.form)
          .then(res => {
            if (res.data.code === 200) {
              this.$message({
                message: '添加成功',
                type: 'success'
              })
              this.dialogManage = false
              this.get_jurisdictions()
            } else {
              this.$message.error(res.data.msg)
            }
            this.loading = false
          })
          .catch(err => {
            this.$message.error(err)
            this.loading = false
          })
      }
    },
    handleEdit(val) {
      this.form = val
      this.dialogTitle = '更新权限'
      this.dialogManage = true
    },
    handleDelete(val) {
      this.$confirm('此操作将永久删除该权限, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      })
        .then(() => {
          this.loading = true
          this.axios
            .delete(`${this.url}/jurisdiction/${val.id}/`)
            .then(res => {
              if (res.data.code === 200) {
                this.$message({
                  message: '删除成功',
                  type: 'success'
                })
                this.get_jurisdictions()
              } else {
                this.$message.error(res.data.msg)
              }
              this.loading = false
            })
            .catch(err => {
              this.$message.error(err)
              this.loading = false
            })
        })
        .catch(() => {
          this.$message({
            type: 'info',
            message: '已取消删除'
          })
        })
    },
    close() {
      this.form = {}
      this.dialogManage = false
    },
    get_jurisdictions() {
      this.loading = true
      this.axios
        .get(`${this.url}/jurisdiction/`)
        .then(res => {
          if (res.data.code === 200) {
            this.jurisdictions = res.data.data
          } else {
            this.$message.error(res.data.msg)
          }
          this.loading = false
        })
        .catch(err => {
          this.$message.error(err)
          this.loading = false
        })
    }
  },
  mounted() {
    this.get_jurisdictions()
  }
}
</script>

<style lang="scss" scoped>
#jurisdiction {
  width: 100%;
  height: 100%;
  padding: 40px;
  .title {
    display: flex;
    justify-content: space-between;
  }
}
</style>
