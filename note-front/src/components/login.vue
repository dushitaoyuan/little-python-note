<template>
  <div v-show="loginShow">
    <el-form :label-position="labelPosition" :rules="rules" ref="loginForm" label-width="80px" :model="loginForm">
      <el-form-item label="账户名" prop="username">
        <el-input v-model="loginForm.username"></el-input>
      </el-form-item>
      <el-form-item label="密码" prop="password">
        <el-input type="password" v-model="loginForm.password"></el-input>
      </el-form-item>
      <el-form-item label="一周免登录">
        <el-switch v-model="loginForm.remember"></el-switch>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="login('loginForm')">登录</el-button>
        <el-button @click="reset('loginForm')">重置</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
  export default {
    name: "login",
    data() {
      return {
        labelPosition: 'top',
        loginShow: true,
        loginForm: {
          username: '',
          password: '',
          remember: false
        },
        rules: {
          username: [
            {required: true, message: '请输入账户名', trigger: 'blur'}
          ],
          password: [
            {required: true, message: '请输入密码', trigger: 'change'}
          ]

        }
      };
    },
    mounted() {
      //如果 已登录,或已设置免密登录 不显示登录页
      if (!this.authApi.isLogin()) {
        this.loginShow = false;
        if (this.authApi.isRemermber()) {
          this.authApi.autoRemmeberLogin();
          this.$router.push("/index")
        }
      }

    },
    methods: {
      login(formName) {
        var that = this
        this.$refs[formName].validate((valid) => {
          if (valid) {
            that.authApi.auth(that.loginForm)
          }
        });
      },
      reset(formName) {
        this.$refs[formName].resetFields();
      }
    }
  }
</script>

<style scoped>

</style>
