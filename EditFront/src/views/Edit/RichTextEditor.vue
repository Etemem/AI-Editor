<template>
    <div class="rich-text-editor">
      <editor-content :editor="editor" />
    </div>
  </template>
  
  <script setup>
  import { useEditor, EditorContent } from '@tiptap/vue-3'
  import StarterKit from '@tiptap/starter-kit'
  
  const props = defineProps({
    content: {
      type: String,
      default: '',
    },
  })
  
  const emit = defineEmits(['update:content'])
  
  const editor = useEditor({
    content: props.content,
    extensions: [StarterKit],
    onUpdate: ({ editor }) => {
      emit('update:content', editor.getHTML())
    },
  })
  </script>
  
  <style scoped>
  .rich-text-editor {
    height: 100%;
    overflow-y: auto;
  }
  </style>