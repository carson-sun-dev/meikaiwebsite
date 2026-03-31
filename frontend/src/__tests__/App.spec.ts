import { describe, it, expect } from 'vitest'
import { flushPromises, mount } from '@vue/test-utils'
import { createRouter, createMemoryHistory } from 'vue-router'

import App from '../App.vue'
import TestView from '../views/Home.vue'

describe('App', () => {
  it('mounts and shows landing content via router', async () => {
    const router = createRouter({
      history: createMemoryHistory(),
      routes: [
        { path: '/', redirect: '/home' },
        { path: '/home', component: TestView },
      ],
    })
    await router.push('/')
    await router.isReady()

    const wrapper = mount(App, {
      global: { plugins: [router] },
    })
    await flushPromises()

    expect(wrapper.text()).toContain('以匠心')
  })
})
