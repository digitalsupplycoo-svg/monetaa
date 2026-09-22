import {defineField, defineType} from 'sanity'

export default defineType({
  name: 'siteSettings',
  title: 'Site settings',
  type: 'document',
  fields: [
    defineField({
      name: 'heroHeading',
      title: 'Homepage headline',
      description: 'The big heading on the homepage, e.g. "MIND YOUR MONEY".',
      type: 'string',
    }),
    defineField({
      name: 'heroSubtitle',
      title: 'Homepage subheading',
      type: 'string',
    }),
    defineField({
      name: 'contactEmail',
      title: 'Contact email',
      description: 'Shown on the Contact page. Leave empty to hide it.',
      type: 'string',
    }),
    defineField({
      name: 'adsenseClient',
      title: 'AdSense publisher ID',
      description: 'e.g. ca-pub-1234567890123456',
      type: 'string',
    }),
  ],
  preview: {
    prepare() {
      return {title: 'Site settings'}
    },
  },
})
