import {defineConfig} from 'sanity'
import {structureTool} from 'sanity/structure'
import {visionTool} from '@sanity/vision'
import {schemaTypes} from './schemaTypes'
import {structure} from './structure'

const SINGLETON_TYPES = new Set(['siteSettings'])

export default defineConfig({
  name: 'default',
  title: 'Moneta Blog',

  projectId: 'auge2q4g',
  dataset: 'production',

  plugins: [structureTool({structure}), visionTool()],

  schema: {
    types: schemaTypes,
  },

  document: {
    actions: (prev, context) =>
      SINGLETON_TYPES.has(context.schemaType)
        ? prev.filter(
            ({action}) => action && !['duplicate', 'delete'].includes(action)
          )
        : prev,
    newDocumentOptions: (prev, context) =>
      prev.filter(
        (template) => !SINGLETON_TYPES.has(template.templateId)
      ),
  },
})
