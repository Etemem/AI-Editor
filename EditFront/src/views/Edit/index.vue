<template>
  <div class="MainContainer">
    <div class="TopRow">
      <h1 class="WebsiteName">AI Smart Editor</h1>
    </div>
    <div class="EditMain" ref="filecont">
      <div class="lefttools">
        <LeftToolbar />
      </div>
      <div class="editor">
        <div class="editorcard">
          <div class="toptools">
            <EditorMenu :editor="editor" />
            <el-switch
              v-model="editorMode"
              active-text="Rich Text"
              inactive-text="Table"
              @change="switchEditorMode"
            />
          </div>
          <div class="editcont">
            <RichTextEditor v-if="editorMode === 'richText'" v-model:content="content" />
            <TableEditor v-else v-model:data="tableData" />
          </div>
          <div class="bottomcount" v-if="editorMode === 'richText'">
            字数统计: {{ characterCount }}
          </div>
        </div>
      </div>
      <div class="righttools">
        <Outline></Outline>
      </div>
    </div>
  </div>
</template>
  <script lang="ts" setup>
  import {Brush,EditPen,} from '@element-plus/icons-vue'
  import { defineComponent, onMounted, onBeforeUnmount, ref,watch } from 'vue';
  import { Editor, EditorContent, useEditor, BubbleMenu  } from '@tiptap/vue-3';
  import { storeToRefs } from 'pinia'
  import Underline from '@tiptap/extension-underline'
  // 列表
  import ListItem from '@tiptap/extension-list-item'
  import OrderedList from '@tiptap/extension-ordered-list'
  import BulletList from '@tiptap/extension-bullet-list'
  // 代码
  import CodeBlockLowlight from '@tiptap/extension-code-block-lowlight'
  import css from 'highlight.js/lib/languages/css'
  import js from 'highlight.js/lib/languages/javascript'
  import ts from 'highlight.js/lib/languages/typescript'
  import html from 'highlight.js/lib/languages/xml'
  import { common, createLowlight } from 'lowlight'
  // 字数统计
  import CharacterCount from '@tiptap/extension-character-count'
  import Heading from '@tiptap/extension-heading'
  import StarterKit from '@tiptap/starter-kit'
  import Placeholder from '@tiptap/extension-placeholder'
  import { UndoRound, MoreHorizOutlined } from '@vicons/material'
  import TaskItem from '@tiptap/extension-task-item'
  import TaskList from '@tiptap/extension-task-list'
  import Outline from './Outline/index.vue'
    // 使用Pinia
  import { useEditorStore } from '@/Store'
  import EditorMenu from './EditorMenu/index.vue'
  import { defineStore } from 'pinia'
  import { ElMessage } from 'element-plus';
  import axios from 'axios'
 
  import LeftToolbar from './LeftToolbar/LeftToolbar.vue';
  import RichTextEditor from './RichTextEditor.vue'
  import TableEditor from './TableEditor.vue'

  const editorStore = useEditorStore()
  const editorMode = ref('richText')
  const content = ref('')
  const tableData = ref([{ A: '', B: '' }])

  const characterCount = computed(() => {
    return content.value.replace(/<[^>]*>/g, '').length
  })

  const switchEditorMode = (mode) => {
    editorMode.value = mode
    // You might want to add logic here to convert between rich text and table data
  }


  const lowlight = createLowlight()
  lowlight.register({ html, ts, css, js })

    const aipolish = ref("")
    const filecont = ref(null);
    const aicontinuation = ref("")
    const visiblemenu = ref(false)
    const position = ref({
          top: 0,
          left: 0
    })
    var hasmove=ref(false);
    var hisstring:any;
    var selection:any;
    //进行润色的函数
      //进行润色的函数
  const polish=()=>{
    visiblemenu.value = false;
    let formData = new FormData();
    formData.append("username","123456");
    formData.append("key","1448c89ed7a84bf7f696097eaf645ab7f6ca822d");
    formData.append("cont",hisstring);
    let url = 'http://127.0.0.1:5000/getpolish' //访问后端接口的url
    let method = 'post'
    axios({
      method,
      url,
      data: formData,
    }).then(res => {
      alert(res.data.answer)
      console.log(res.data.answer);
    });
  }
//进行aiaireview
  const continuation=()=>{
    visiblemenu.value = false;
    let formData = new FormData();
    formData.append("username","123456");
    formData.append("key","1448c89ed7a84bf7f696097eaf645ab7f6ca822d");
    formData.append("cont",hisstring);
    let url = 'http://127.0.0.1:5000/getcontinuation' //访问后端接口的url
    let method = 'post'
    axios({
      method,
      url,
      data: formData,
      }).then(res => {
        alert(res.data.answer)
        console.log(res.data.answer);
      });
  }  

  //进行translate
  const translation=()=>{
    visiblemenu.value = false;
    let formData = new FormData();
    formData.append("username","123456");
    formData.append("key","1448c89ed7a84bf7f696097eaf645ab7f6ca822d");
    formData.append("cont",hisstring);
    let url = 'http://127.0.0.1:5000/gettranslation' //访问后端接口的url
    let method = 'post'
    axios({
      method,
      url,
      data: formData,
      }).then(res => {
        alert(res.data.answer)
        console.log(res.data.answer);
      });
  }  

  //进行summarize
  const summarize=()=>{
    visiblemenu.value = false;
    let formData = new FormData();
    formData.append("username","123456");
    formData.append("key","1448c89ed7a84bf7f696097eaf645ab7f6ca822d");
    formData.append("cont",hisstring);
    let url = 'http://127.0.0.1:5000/getsummarize' //访问后端接口的url
    let method = 'post'
    axios({
      method,
      url,
      data: formData,
      }).then(res => {
        alert(res.data.answer)
        console.log(res.data.answer);
      });
  }  
  //进行proofread
  const proofread=()=>{
    visiblemenu.value = false;
    let formData = new FormData();
    formData.append("username","123456");
    formData.append("key","1448c89ed7a84bf7f696097eaf645ab7f6ca822d");
    formData.append("cont",hisstring);
    let url = 'http://127.0.0.1:5000/getproofread' //访问后端接口的url
    let method = 'post'
    axios({
      method,
      url,
      data: formData,
      }).then(res => {
        alert(res.data.answer)
        console.log(res.data.answer);
      });
  }
    // 获取选中的文字
    const selecttext= (e:MouseEvent)=>{
            selection = window.getSelection();
            if(selection!=null&&hisstring!=selection){
              var content = selection.toString();
              if(content!=""){
                  var rect = filecont.value.getBoundingClientRect();
                  visiblemenu.value = true
                  // alert(e.clientY)
                  // alert(e.clientX)
                  position.value.top =  e.clientY;
                  position.value.left =e.clientX;
                  hisstring=content
                }
              // alert(content)
            }
            else{
              hisstring=""
            }
      }
    //鼠标移动
    const mousemove=()=>{
            hasmove.value=true;
      }
    //鼠标点击
    //const notsee=()=>{
    //        visiblemenu.value = false;
    //        // selection.value="";
    //  }
    // 隐藏菜单的函数
    // 添加隐藏菜单函数
const notsee = () => {
  visiblemenu.value = false;
};

    const see=()=>{
            visiblemenu.value = true;
            // selection.value="";
      }
    //滚轮滚动
    const hasscroll=()=>{
            visiblemenu.value = false;
            // window.getSelection().removeAllRanges()
      }
    const editorStore = useEditorStore()
     // 加载headings
    const loadHeadings = () => {
          const headings = [] as any[]
          if (!editor.value) return
          const transaction = editor.value.state.tr
          if (!transaction) return

          editor.value?.state.doc.descendants((node, pos) => {
            if (node.type.name === 'heading') {
              console.log(pos, node)
              const start = pos
              const end = pos + node.content.size
              // const end = pos + node
              const id = `heading-${headings.length + 1}`
              if (node.attrs.id !== id) {
                transaction?.setNodeMarkup(pos, undefined, {
                  ...node.attrs,
                  id
                })
              }

              headings.push({
                level: node.attrs.level,
                text: node.textContent,
                start,
                end,
                id
              })
            }
          })

          transaction?.setMeta('addToHistory', false)
          transaction?.setMeta('preventUpdate', true)

          editor.value?.view.dispatch(transaction)
          editorStore.setHeadings(headings)
      }
    // 使用ref创建可变的响应式引用
    // 编辑器初始化
    const editor = useEditor({
          content: ``,
          extensions: [
          StarterKit.configure({
              heading: {
                levels: [1, 2, 3,4,5],
              },
            }),
            TaskList,
            TaskItem,
            Placeholder.configure({
              placeholder: '开始输入文本 …'
            }),
            OrderedList,
            BulletList,
            ListItem,
            CharacterCount.configure({
            limit: 10000
          })
          ],
          onUpdate({ edit }) {
            loadHeadings()
            editorStore.setEditorInstance(editor.value)
          },
          onCreate({ edit }) {
            loadHeadings()
            editorStore.setEditorInstance(editor.value)
          },
          injectCSS: false,

      })
  </script>
  <style>
  .MainContainer {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

.TopRow {
  background-color: #e6f2ff; /* 淡蓝色背景 */
  height: 40px; /* 调整这里来改变顶部行的高度 */
  display: flex;
  justify-content: center; /* 水平居中 */
  align-items: center; /* 垂直居中 */
}

.WebsiteName {
  font-family: 'Comic Sans MS','Lucida Handwriting', 'Brush Script MT', 'Segoe Script',  cursive;
  font-size: 1.8rem;
  color: #2c3e50; /* 更鲜明的颜色 */
  margin: 0;
  padding: 0;
}

  .EditMain{
    position: relative;
    width:100vw;
    height: 100vh;

    display: grid;
    grid-template-columns: 20% 60% 20%;
  
  }
  /* 两者选一即可*/
  .EditMain {
  flex-grow: 1;
  display: grid;
  grid-template-columns: 20% 60% 20%;
  }

  .righttools{
    background-color: #f0f2f5;
    height: 100%;
    width: 100%;
  }
  .editor{
 
  }
  .editorcard{
    position: relative;
    width:95%;
    height: 95%;
    left: 2.5%;
    top:2.5%;
    display: grid;
    grid-template-rows: 5% 92% 3%;
    border: 1px solid #4f5c5765;
  }
  .editorcard .editor{
    position: relative;
    width:100%;
    height: 100%;
    left: 0;
    top:0;
    display: grid;
    grid-template-rows: 10% 90%;
  }
  .editorcard .editor{
    position: relative;
    width:100%;
    height: 100%;
    left: 0;
    top:0;
    display: grid;
    grid-template-rows: 10% 90%;
  }
  .toptools{
    background-color: rgba(207, 220, 245, 0.199);
    border-bottom: 1px dashed #9ca19f65;
  }
  .bottomcount{
    background-color: rgba(207, 220, 245, 0.199);
    border-top: 1px dashed #9ca19f65;
    height: 100%;
    width: 100%;
    display: grid;
    grid-template-columns: 100%;
    grid-template-rows: 100%;
    justify-items: center;
    align-items: center;
  }
  .editcont{
    position: relative;
    width: 100%;
    height: 100%;
    overflow: hidden;
  }
  .lefttools {
  background-color: #f0f2f5;
  height: 100%;
  width: 100%;
  overflow-y: auto;
}
  </style>
  
  <style lang="scss">
  b {
    font-weight: bold;
  }
  .ProseMirror {
    overflow-y: scroll;
  }
  .ProseMirror p {
    margin: 0;
  }
  .ProseMirror:focus {
    outline: none;
  }
  .tiptap p.is-editor-empty:first-child::before {
    color: #adb5bd;
    content: attr(data-placeholder);
    float: left;
    height: 0;
    pointer-events: none;
  }
  
  .tiptap {
    > * + * {
      margin-top: 0.75em;
    }
  
    ul {
      padding: 0 2rem;
      list-style: square;
    }
    ol {
      padding: 0 2rem;
      list-style: decimal;
    }
    table {
      border-collapse: collapse;
      table-layout: fixed;
      width: 100%;
      margin: 0;
      overflow: hidden;
  
      td,
      th {
        min-width: 1em;
        border: 2px solid #ced4da;
        padding: 3px 5px;
        vertical-align: top;
        box-sizing: border-box;
        position: relative;
  
        > * {
          margin-bottom: 0;
        }
      }
  
      th {
        font-weight: bold;
        text-align: left;
        background-color: #f1f3f5;
      }
  
      .selectedCell:after {
        z-index: 2;
        position: absolute;
        content: '';
        left: 0;
        right: 0;
        top: 0;
        bottom: 0;
        background: rgba(200, 200, 255, 0.4);
        pointer-events: none;
      }
  
      .column-resize-handle {
        position: absolute;
        right: -2px;
        top: 0;
        bottom: -2px;
        width: 4px;
        background-color: #adf;
        pointer-events: none;
      }
  
      p {
        margin: 0;
      }
    }
    pre {
      background: #0d0d0d;
      color: #fff;
      font-family: 'JetBrainsMono', monospace;
      padding: 0.75rem 1rem;
      border-radius: 0.5rem;
  
      code {
        color: inherit;
        padding: 0;
        background: none;
        font-size: 0.8rem;
      }
  
      .hljs-comment,
      .hljs-quote {
        color: #616161;
      }
  
      .hljs-variable,
      .hljs-template-variable,
      .hljs-attribute,
      .hljs-tag,
      .hljs-name,
      .hljs-regexp,
      .hljs-link,
      .hljs-name,
      .hljs-selector-id,
      .hljs-selector-class {
        color: #f98181;
      }
      .hljs-number,
      .hljs-meta,
      .hljs-built_in,
      .hljs-builtin-name,
      .hljs-literal,
      .hljs-type,
      .hljs-params {
        color: #fbbc88;
      }
  
      .hljs-string,
      .hljs-symbol,
      .hljs-bullet {
        color: #b9f18d;
      }
  
      .hljs-title,
      .hljs-section {
        color: #faf594;
      }
  
      .hljs-keyword,
      .hljs-selector-tag {
        color: #70cff8;
      }
  
      .hljs-emphasis {
        font-style: italic;
      }
  
      .hljs-strong {
        font-weight: 700;
      }
    }
  }
  
  .tableWrapper {
    overflow-x: auto;
  }
  
  .resize-cursor {
    cursor: ew-resize;
    cursor: col-resize;
  }
  .contextmenu {
    width: 120px;
    margin: 0;
    background: #fff;
    z-index: 3000;
    position: absolute;
    list-style-type: none;
    padding:5px;
    padding-left: 15px;
    border-radius: 4px;
    font-size: 12px;
    font-weight: 400;
    color: #333;
    box-shadow: 1px 1px 2px 1px rgba(0, 0, 0, 0.3);
    display: grid;
    grid-template-columns:50% 50%;

  }
  .contextmenu .item {
      height: 35px;
      width:100%;
      line-height: 35px;
      color: rgb(29, 33, 41);
      cursor: pointer;
    }
    .contextmenu .item {
      height: 35px;
      width:100%;
      line-height: 35px;
      color: rgb(29, 33, 41);
      cursor: pointer;
    }

    .contextmenu .item:hover {
      background: rgb(229, 230, 235);
    }
  </style>
