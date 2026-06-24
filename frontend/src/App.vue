<script setup lang="ts">
import { defineAsyncComponent } from 'vue'
import { useHead } from '@unhead/vue'
import { useRoute } from 'vue-router'

import NavigationBar from '@/components/navigationBar.vue'
import { canonicalUrl, getSeoForRoute, ogImageUrl, organizationJsonLd } from '@/seo/seoConfig'

const ChatWidget = defineAsyncComponent(() => import('@/components/ChatWidget/ChatWidget.vue'))

const route = useRoute()

useHead(() => {
  const seo = getSeoForRoute(route.name)
  const canonical = canonicalUrl(route.path)
  const ogImg = ogImageUrl()
  const meta: Array<Record<string, string>> = [
    { name: 'description', content: seo.description },
    { name: 'keywords', content: seo.keywords },
    { property: 'og:title', content: seo.title },
    { property: 'og:description', content: seo.description },
    { property: 'og:type', content: 'website' },
    { property: 'og:locale', content: 'zh_CN' },
    { property: 'og:site_name', content: '河南美恺装饰' },
    // og:image:微信/QQ/Facebook 抓的就是它;固定指向公司带字 logo
    { property: 'og:image', content: ogImg },
    { property: 'og:image:alt', content: '河南美恺装饰' },
    // Twitter Card(海外渠道兼容,百度不读但无害)
    { name: 'twitter:card', content: 'summary_large_image' },
    { name: 'twitter:title', content: seo.title },
    { name: 'twitter:description', content: seo.description },
    { name: 'twitter:image', content: ogImg },
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
  <NavigationBar />
  <router-view />
  <ChatWidget />
</template>

<style scoped></style>
