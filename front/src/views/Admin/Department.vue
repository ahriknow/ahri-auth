<template>
  <div
    id="department"
    class="department"
    v-loading="loading"
    element-loading-text="拼命加载中"
    element-loading-spinner="el-icon-loading"
    element-loading-background="rgba(0, 0, 0, 0.8)"
  >
    <div class="title">
      <h2>分组列表</h2>
      <el-button @click="dialogVisible = true">添 加</el-button>
    </div>
    <el-divider></el-divider>
    <el-input placeholder="输入关键字进行过滤" size="medium" v-model="filterText" style="margin-bottom: 20px"></el-input>
    <el-tree
      ref="tree"
      :data="departments"
      node-key="id"
      :expand-on-click-node="false"
      default-expand-all
      :filter-node-method="filterNode"
    >
      <span class="custom-tree-node" slot-scope="{ node, data }">
        <span>
          {{ node.data.name }}
          <span class="describe">{{ node.data.describe }}</span>
        </span>
        <span>
          <el-button type="text" size="mini" @click="() => append(data)">添加子部门</el-button>
          <el-button type="text" size="mini" @click="() => update(data)">更新部门</el-button>
          <el-button type="text" size="mini" @click="() => remove(data)">删除部门</el-button>
          <el-button type="text" size="mini" @click="() => manage(data)">权限管理</el-button>
        </span>
      </span>
    </el-tree>
    <el-dialog title="部门管理" :visible.sync="dialogVisible" @close="close">
      <el-form :model="form" label-width="80px" style="margin-right: 40px">
        <el-form-item label="部门名称">
          <el-input v-model="form.name" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="部门描述">
          <el-input v-model="form.describe" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="父级部门">
          <el-input v-model="form.p_name" autocomplete="off" disabled></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="add()">确 定</el-button>
      </div>
    </el-dialog>
    <el-dialog title="权限管理" :visible.sync="dialogManage" width="800px">
      <el-transfer
        :titles="['所有权限', '部门权限']"
        filterable
        :filter-method="filterMethod"
        filter-placeholder="请输入权限搜索"
        v-model="value"
        :data="jurisdictions"
      ></el-transfer>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogManage = false">取 消</el-button>
        <el-button type="primary" @click="handlerManage">确 定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: 'department',
  data() {
    return {
      filterText: '',
      departments: [],
      jurisdictions: [],
      dialogVisible: false,
      dialogManage: false,
      loading: false,
      form: {
        name: '',
        describe: '',
        parent: null,
        p_name: '顶级部门'
      },
      value: [],
      filterMethod(query, item) {
        return item.name.indexOf(query) > -1
      },
      current: {}
    }
  },
  methods: {
    filterNode(value, data) {
      if (!value) return true
      return data.name.indexOf(value) !== -1
    },
    handlerManage() {
      this.loading = true
      this.axios
        .put(`${this.url}/department/${this.current.id}/`, {
          jurisdiction: this.value
        })
        .then(res => {
          if (res.data.code === 200) {
            this.$message({
              message: '更新成功',
              type: 'success'
            })
            this.dialogManage = false
            this.$store.commit('refresh', new Date().getTime())
            this.get_departments()
          } else {
            this.$message.error(res.data.msg)
          }
          this.loading = false
        })
        .catch(err => {
          this.$message.error(err)
          this.loading = false
        })
    },
    getJsonTree(data, parentId) {
      var itemArr = []
      for (var i = 0; i < data.length; i++) {
        var node = data[i]
        if (node.parent == parentId) {
          var newNode = {}
          newNode.id = node.id
          newNode.name = node.name
          newNode.describe = node.describe
          newNode.jurisdiction = node.jurisdiction
          newNode.p_name = node.p_name
          newNode.children = this.getJsonTree(data, node.id)
          itemArr.push(newNode)
        }
      }
      return itemArr
    },
    update(data) {
      this.form = data
      this.dialogVisible = true
    },
    append(data) {
      this.form.parent = data.id
      this.form.p_name = data.name
      this.dialogVisible = true
    },
    close() {
      this.form = {
        name: '',
        describe: '',
        parent: null,
        p_name: '顶级部门'
      }
      this.dialogVisible = false
    },
    add() {
      if (this.form.hasOwnProperty('id')) {
        this.loading = true
        this.axios
          .put(`${this.url}/department/${this.form.id}/`, this.form)
          .then(res => {
            if (res.data.code === 200) {
              this.$message({
                message: '更新成功',
                type: 'success'
              })
              this.get_departments()
              this.dialogVisible = false
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
          .post(`${this.url}/department/`, this.form)
          .then(res => {
            if (res.data.code === 200) {
              this.$message({
                message: '添加成功',
                type: 'success'
              })
              this.get_departments()
              this.dialogVisible = false
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
    remove(data) {
      this.$confirm('此操作将永久删除该部门及其下属部门, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      })
        .then(() => {
          this.loading = true
          this.axios
            .delete(`${this.url}/department/${data.id}/`)
            .then(res => {
              if (res.data.code === 200) {
                this.$message({
                  message: '删除成功',
                  type: 'success'
                })
                this.get_departments()
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
    manage(data) {
      this.value = data.jurisdiction
      this.current = data
      this.dialogManage = true
    },
    get_departments() {
      this.loading = true
      this.axios
        .get(`${this.url}/department/`)
        .then(res => {
          if (res.data.code === 200) {
            this.departments = this.getJsonTree(res.data.data, null)
          } else {
            this.$message.error(res.data.msg)
          }
          this.loading = false
        })
        .catch(err => {
          this.$message.error(err)
          this.loading = false
        })
    },
    get_jurisdictions() {
      this.loading = true
      this.axios
        .get(`${this.url}/jurisdiction/`)
        .then(res => {
          if (res.data.code === 200) {
            res.data.data.forEach(item => {
              this.jurisdictions.push({
                label: item.name,
                key: item.id,
                name: item.name
              })
            })
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
    this.get_departments()
    this.get_jurisdictions()
  },
  watch: {
    filterText(val) {
      this.$refs.tree.filter(val)
    }
  }
}
</script>

<style lang="scss" scoped>
#department {
  width: 100%;
  height: 100%;
  padding: 40px;
  .title {
    display: flex;
    justify-content: space-between;
  }
  .custom-tree-node {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 20px;
    padding-right: 8px;
    .describe {
      font-size: 14px;
      padding-left: 20px;
      overflow: hidden;
    }
  }
  .el-transfer {
    width: 600px;
    margin: 0 auto;
  }
}
</style>
