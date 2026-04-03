<script setup lang="ts">
import { useHead } from '@unhead/vue'
import { useRoute } from 'vue-router'

import { canonicalUrl, getSeoForRoute, organizationJsonLd } from '@/seo/seoConfig'

const route = useRoute()

useHead(() => {
  const seo = getSeoForRoute(route.name)
  const canonical = canonicalUrl(route.path)
  const meta: Array<Record<string, string>> = [
    { name: 'description', content: seo.description },
    { name: 'keywords', content: seo.keywords },
    { property: 'og:title', content: seo.title },
    { property: 'og:description', content: seo.description },
    { property: 'og:type', content: 'website' },
    { property: 'og:locale', content: 'zh_CN' },
  ]
  if (canonical) {
    meta.push({ property: 'og:url', content: canonical })
  }
  return {
    htmlAttrs: {
      lang: 'zh-CN',
    },
    title: seo.title,
    meta,
    link: canonical ? [{ rel: 'canonical', href: canonical }] : [],
    script: [
      {
        key: 'jsonld-organization',
        type: 'application/ld+json',
        children: JSON.stringify(organizationJsonLd()),
      },
    ],
  }
})
</script>

<template>
  <router-view />
</template>

<style scoped></style>
