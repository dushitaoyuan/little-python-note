<template>
  <div>

    <el-container>
      <el-aside>
        <el-tree
          :props="props"
          :load="loadNode"
          lazy
          @node-click="detail"
        >
        </el-tree>


      </el-aside>
      <el-container>
        <el-header>
          <div>
            {{noteDetail.title?noteDetail.title:noteDetail.name}}<br/>
            <small v-show="!noteDetail.category && noteDetail.create_time">发布时间:{{noteDetail.create_time}}</small>
          </div>
        </el-header>
        <el-main>
          <markdown-it-vue class="md-body" :content="noteContent"/>
        </el-main>
        <el-footer>by dushitaoyuan</el-footer>
      </el-container>
    </el-container>
  </div>
</template>

<script>
  import MarkdownItVue from 'markdown-it-vue'
  import 'markdown-it-vue/dist/markdown-it-vue.css'

  export default {
    name: "index",
    components: {
      MarkdownItVue
    },
    data() {
      return {
        noteList: [],
        noteDetail: {},
        noteContent: "",
        props: {
          label: 'name',
          children: 'zones',
          isLeaf: 'leaf'
        },

      };
    },
    mounted() {
      this.list()
    },
    methods: {
      loadNode(node, resolve) {
        var noteListUrl = this.$axios.VIRTUAL_BASE_PATH + "note/list";
        if (node.data && node.data.path) {
          noteListUrl += "?noteDirPath=" + node.data.path;
        }
        var that = this;
        this.$axios
          .get(noteListUrl)
          .then(res => {
            that.noteList = res.data.data;
            if (that.noteList.length > 0) {
              that.noteDetail = that.noteList[0]
              for (var i = 0; i < that.noteList.length; i++) {
                if (that.noteList[i].category) {
                  that.noteList[i].leaf = false;
                } else {
                  that.noteList[i].leaf = true;
                }
              }
              resolve(that.noteList)
            }
          });
      },
      detail(note) {
        let that = this;
        that.noteDetail = note
        if (note.category) {
          that.noteContent = "";
        }
        this.$axios
          .get(this.$axios.VIRTUAL_BASE_PATH + "note?notePath=" + note.path)
          .then(res => {
            that.noteContent = res.data.data;
          });
      }
    }
  }
</script>

<style scoped>
  .el-header {
    background-color: #fff;
    color: #333;
    text-align: center;
    height: 60px;
    font-weight: bolder;
    line-height: 30px;
  }

  .el-header small {
    color: gray;
  }


  .el-aside {
    background-color: #fff;
    color: #333;
    text-align: center;
    height: 920px;
    width: 150px;
  }

  .el-main {
    background-color: #fff;
    color: #333;
    text-align: center;
    height: 800px;
  }

  .el-footer {
    background-color: #B3C0D1;
    color: #333;
    text-align: center;
    height: 30px;
    font-size: 20px;
    line-height: 30px;
    font-weight: bolder;
    bottom: 0;
    width: 100%;
  }


</style>
