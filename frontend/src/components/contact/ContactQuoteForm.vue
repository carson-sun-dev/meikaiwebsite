<template>
  <section class="contact-quote">
    <div class="contact-quote__wrap">
      <h1 class="contact-quote__title">我的工程需要多少费用？</h1>

      <div class="contact-quote__plans" role="radiogroup" aria-label="选择服务类型">
        <button
          v-for="p in planList"
          :key="p.key"
          type="button"
          class="contact-plan"
          :class="{ 'contact-plan--active': selectedPlan === p.key }"
          :aria-checked="selectedPlan === p.key"
          role="radio"
          @click="selectedPlan = p.key"
        >
          <div class="contact-plan__title">{{ p.title }}</div>
        </button>
      </div>

      <form class="contact-quote__form" @submit.prevent="onSubmit">
        <div class="contact-quote__section-title">通用</div>
        <div class="contact-quote__grid">
          <div class="contact-quote__field">
            <label class="contact-quote__label contact-quote__label--required" for="building-type">
              建筑类型（新建/翻新）
            </label>
            <div class="contact-quote__select">
              <select
                id="building-type"
                v-model="buildingType"
                aria-label="建筑类型"
                aria-required="true"
              >
                <option disabled value="">请选择</option>
                <option value="new">新建</option>
                <option value="renovation">翻新</option>
                <option value="other">其他</option>
              </select>
              <span class="contact-quote__select-arrow" aria-hidden="true" />
            </div>
          </div>

          <div class="contact-quote__field">
            <label class="contact-quote__label contact-quote__label--required" for="schedule">预计工期</label>
            <div class="contact-quote__select">
              <select id="schedule" v-model="schedule" aria-label="预计工期" aria-required="true">
                <option disabled value="">请选择</option>
                <option value="1">少于1个月</option>
                <option value="1-3">1月-3月</option>
                <option value="4-6">4月-6月</option>          
                <option value="other">其他</option>
              </select>
              <span class="contact-quote__select-arrow" aria-hidden="true" />
            </div>
          </div>
        </div>

        <!-- 店铺 -->
        <div v-if="selectedPlan === 'store'" class="contact-quote__plan-block">
          <div class="contact-quote__section-title contact-quote__section-title--tight">工程细节</div>
          <div class="contact-quote__grid">
            <div class="contact-quote__field">
              <label class="contact-quote__label contact-quote__label--required" for="store-type">
                店铺类型（餐饮、零售等）
              </label>
              <div class="contact-quote__select">
                <select id="store-type" v-model="storeType" aria-label="店铺类型" aria-required="true">
                  <option disabled value="">请选择</option>
                  <option value="food">餐饮</option>
                  <option value="retail">品牌零售</option>
                  <option value="entertainment">娱乐（酒吧/KTV/密室逃脱等）</option>
                  <option value="fitness">健身房</option>
                  <option value="milk-tea">奶茶店</option>
                  <option value="other">其他</option>
                </select>
                <span class="contact-quote__select-arrow" aria-hidden="true" />
              </div>
            </div>

            <div class="contact-quote__field">
              <label class="contact-quote__label contact-quote__label--required" for="shop-area">门店总面积</label>
              <div class="contact-quote__select">
                <select id="shop-area" v-model="shopArea" aria-label="营业面积" aria-required="true">
                  <option disabled value="">请选择</option>
                  <option value="lt50">50㎡以下</option>
                  <option value="50-100">50-100㎡</option>
                  <option value="100-200">100-200㎡</option>
                  <option value="gt200">200㎡以上</option>
                  <option value="other">其他</option>
                </select>
                <span class="contact-quote__select-arrow" aria-hidden="true" />
              </div>
            </div>

            <div class="contact-quote__field">
              <label class="contact-quote__label" for="back-area">门店面积（后厨/仓库面积）</label>
              <div class="contact-quote__select">
                <select id="back-area" v-model="backArea" aria-label="后厨/仓库面积">
                  <option disabled value="">请选择</option>
                  <option value="lt20">20㎡以下</option>
                  <option value="20-50">20-50㎡</option>
                  <option value="50-100">50-100㎡</option>
                  <option value="gt100">100㎡以上</option>
                  <option value="other">其他</option>
                </select>
                <span class="contact-quote__select-arrow" aria-hidden="true" />
              </div>
            </div>

            <div class="contact-quote__field contact-quote__field--full">
              <span class="contact-quote__label">门头需求（可多选）</span>
              <details class="contact-quote__fold">
                <summary class="contact-quote__fold-summary">
                  <span class="contact-quote__fold-hint">{{ summarizeMulti(doorSignNeeds, doorSignOptions) }}</span>
                  <span class="contact-quote__fold-arrow" aria-hidden="true" />
                </summary>
                <div class="contact-quote__fold-panel">
                  <label v-for="opt in doorSignOptions" :key="opt.value" class="contact-quote__check">
                    <input v-model="doorSignNeeds" type="checkbox" :value="opt.value" />
                    {{ opt.label }}
                  </label>
                </div>
              </details>
            </div>

            <div class="contact-quote__field contact-quote__field--full">
              <span class="contact-quote__label">特殊设备（可多选）</span>
              <details class="contact-quote__fold">
                <summary class="contact-quote__fold-summary">
                  <span class="contact-quote__fold-hint">{{ summarizeMulti(specialDevices, specialDeviceOptions) }}</span>
                  <span class="contact-quote__fold-arrow" aria-hidden="true" />
                </summary>
                <div class="contact-quote__fold-panel">
                  <label v-for="opt in specialDeviceOptions" :key="opt.value" class="contact-quote__check">
                    <input v-model="specialDevices" type="checkbox" :value="opt.value" />
                    {{ opt.label }}
                  </label>
                </div>
              </details>
            </div>

            <div class="contact-quote__field">
              <label class="contact-quote__label" for="license-assist">营业执照协助（建筑许可/消防）</label>
              <div class="contact-quote__select">
                <select id="license-assist" v-model="licenseAssist" aria-label="营业执照协助">
                  <option disabled value="">请选择</option>
                  <option value="none">不需要</option>
                  <option value="permit-only">仅建筑许可</option>
                  <option value="fire-only">仅消防</option>
                  <option value="both">两者都需要</option>
                  <option value="other">其他</option>
                </select>
                <span class="contact-quote__select-arrow" aria-hidden="true" />
              </div>
            </div>
          </div>
        </div>

        <!-- 商务·办公 -->
        <div v-if="selectedPlan === 'business'" class="contact-quote__plan-block">
          <div class="contact-quote__section-title contact-quote__section-title--tight">商务·办公</div>
          <div class="contact-quote__grid">
            <div class="contact-quote__field">
              <label class="contact-quote__label contact-quote__label--required" for="work-area">工程面积</label>
              <div class="contact-quote__select">
                <select
                  id="work-area"
                  v-model="businessSeatArea"
                  aria-label="工程面积"
                  aria-required="true"
                >
                  <option disabled value="">请选择</option>
                  <option value="lt100">100㎡以下</option>
                  <option value="100-200">100-200㎡</option>
                  <option value="200-500">200-500㎡</option>
                  <option value="gt500">500㎡以上</option>
                  <option value="other">其他</option>
                </select>
                <span class="contact-quote__select-arrow" aria-hidden="true" />
              </div>
            </div>

            <div class="contact-quote__field">
              <label class="contact-quote__label" for="office-count">独立办公室数量</label>
              <div class="contact-quote__select">
                <select id="office-count" v-model="businessOfficeCount" aria-label="独立办公室数量">
                  <option value="">请选择</option>
                  <option value="1">1间</option>
                  <option value="2-3">2-3间</option>
                  <option value="4-5">4-5间</option>
                  <option value="6+">6间以上</option>
                  <option value="other">其他</option>
                </select>
                <span class="contact-quote__select-arrow" aria-hidden="true" />
              </div>
            </div>

            <div class="contact-quote__field">
              <label class="contact-quote__label" for="meeting-count">会议室数量</label>
              <div class="contact-quote__select">
                <select id="meeting-count" v-model="businessMeetingCount" aria-label="会议室数量">
                  <option disabled value="">请选择</option>
                  <option value="1">1间</option>
                  <option value="2">2间</option>
                  <option value="3+">3间以上</option>
                  <option value="other">其他</option>
                </select>
                <span class="contact-quote__select-arrow" aria-hidden="true" />
              </div>
            </div>

            <div class="contact-quote__field contact-quote__field--full">
              <span class="contact-quote__label">功能分区（前台/茶水间/机房/休息室等，可多选）</span>
              <details class="contact-quote__fold">
                <summary class="contact-quote__fold-summary">
                  <span class="contact-quote__fold-hint">{{ summarizeMulti(businessFuncZones, businessFuncZoneOptions) }}</span>
                  <span class="contact-quote__fold-arrow" aria-hidden="true" />
                </summary>
                <div class="contact-quote__fold-panel">
                  <label v-for="opt in businessFuncZoneOptions" :key="opt.value" class="contact-quote__check">
                    <input v-model="businessFuncZones" type="checkbox" :value="opt.value" />
                    {{ opt.label }}
                  </label>
                </div>
              </details>
            </div>


            <div class="contact-quote__field contact-quote__field--full">
              <span class="contact-quote__label">智能化弱电（网络/门禁/视频会议/背景音乐等，可多选）</span>
              <details class="contact-quote__fold">
                <summary class="contact-quote__fold-summary">
                  <span class="contact-quote__fold-hint">{{ summarizeMulti(businessWeakElectrics, businessWeakElectricOptions) }}</span>
                  <span class="contact-quote__fold-arrow" aria-hidden="true" />
                </summary>
                <div class="contact-quote__fold-panel">
                  <label v-for="opt in businessWeakElectricOptions" :key="opt.value" class="contact-quote__check">
                    <input v-model="businessWeakElectrics" type="checkbox" :value="opt.value" />
                    {{ opt.label }}
                  </label>
                </div>
              </details>
            </div>
            <div class="contact-quote__field">
              <label class="contact-quote__label" for="soundproof">是否需要隔音处理</label>
              <div class="contact-quote__select">
                <select id="soundproof" v-model="businessSoundproof" aria-label="隔音处理">
                  <option value="">请选择</option>
                  <option value="yes">需要</option>
                  <option value="no">不需要</option>
                  <option value="other">其他</option>
                </select>
                <span class="contact-quote__select-arrow" aria-hidden="true" />
              </div>
            </div>

            <div class="contact-quote__field">
              <label class="contact-quote__label" for="ac-type">空调系统</label>
              <div class="contact-quote__select">
                <select id="ac-type" v-model="businessAcType" aria-label="空调系统">
                  <option value="">请选择</option>
                  <option value="independent">独立中央空调</option>
                  <option value="building">楼宇中央空调接入</option>
                  <option value="other">其他</option>
                </select>
                <span class="contact-quote__select-arrow" aria-hidden="true" />
              </div>
            </div>

            <div class="contact-quote__field">
              <label class="contact-quote__label" for="furniture">家具定制（是否包含工位家具采购）</label>
              <div class="contact-quote__select">
                <select id="furniture" v-model="businessFurnitureCustomized" aria-label="家具定制">
                  <option value="">请选择</option>
                  <option value="yes">包含</option>
                  <option value="no">不包含</option>
                  <option value="other">其他</option>
                </select>
                <span class="contact-quote__select-arrow" aria-hidden="true" />
              </div>
            </div>
          </div>
        </div>

        <!-- 家装 -->
        <div v-if="selectedPlan === 'residential'" class="contact-quote__plan-block">
          <div class="contact-quote__section-title contact-quote__section-title--tight">家装</div>
          <div class="contact-quote__grid">
            <div class="contact-quote__field">
              <label class="contact-quote__label contact-quote__label--required" for="res-home-area">房屋面积（建面）</label>
              <div class="contact-quote__select">
                <select
                  id="res-home-area"
                  v-model="resHomeArea"
                  aria-label="房屋面积"
                  aria-required="true"
                >
                  <option disabled value="">请选择</option>
                  <option value="lt80">80㎡以下</option>
                  <option value="80-120">80-120㎡</option>
                  <option value="120-160">120-160㎡</option>
                  <option value="160-200">160-200㎡</option>
                  <option value="gt200">200㎡以上</option>
                  <option value="other">其他</option>
                </select>
                <span class="contact-quote__select-arrow" aria-hidden="true" />
              </div>
            </div>

            <div class="contact-quote__field">
              <label class="contact-quote__label" for="res-bedroom">卧室数量</label>
              <div class="contact-quote__select">
                <select id="res-bedroom" v-model="resBedroomCount" aria-label="卧室数量">
                  <option value="">请选择</option>
                  <option value="1">1</option>
                  <option value="2">2</option>
                  <option value="3">3</option>
                  <option value="other">其他</option>
                </select>
                <span class="contact-quote__select-arrow" aria-hidden="true" />
              </div>
            </div>

            <div class="contact-quote__field">
              <label class="contact-quote__label" for="res-bathroom">卫生间数量</label>
              <div class="contact-quote__select">
                <select id="res-bathroom" v-model="resBathroomCount" aria-label="卫生间数量">
                  <option value="">请选择</option>
                  <option value="1">1</option>
                  <option value="2">2</option>
                  <option value="3">3</option>
                  <option value="other">其他</option>
                </select>
                <span class="contact-quote__select-arrow" aria-hidden="true" />
              </div>
            </div>

            <div class="contact-quote__field">
              <label class="contact-quote__label" for="res-living">客厅数量</label>
              <div class="contact-quote__select">
                <select id="res-living" v-model="resLivingRoomCount" aria-label="客厅数量">
                  <option value="">请选择</option>
                  <option value="1">1</option>
                  <option value="2">2</option>
                  <option value="3">3</option>
                  <option value="other">其他</option>
                </select>
                <span class="contact-quote__select-arrow" aria-hidden="true" />
              </div>
            </div>

            <div class="contact-quote__field">
              <label class="contact-quote__label" for="res-dining">餐厅数量</label>
              <div class="contact-quote__select">
                <select id="res-dining" v-model="resDiningRoomCount" aria-label="餐厅数量">
                  <option value="">请选择</option>
                  <option value="1">1</option>
                  <option value="2">2</option>
                  <option value="3">3</option>
                  <option value="other">其他</option>
                </select>
                <span class="contact-quote__select-arrow" aria-hidden="true" />
              </div>
            </div>

            <div class="contact-quote__field">
              <label class="contact-quote__label" for="island">岛台需求</label>
              <div class="contact-quote__select">
                <select id="island" v-model="resIslandNeed" aria-label="岛台需求">
                  <option value="">请选择</option>
                  <option value="yes">需要</option>
                  <option value="no">不需要</option>
                  <option value="other">其他</option>
                </select>
                <span class="contact-quote__select-arrow" aria-hidden="true" />
              </div>
            </div>


            <div class="contact-quote__field contact-quote__field--full">
              <span class="contact-quote__label">地板和墙面（可多选）</span>
              <details class="contact-quote__fold">
                <summary class="contact-quote__fold-summary">
                  <span class="contact-quote__fold-hint">{{ summarizeMulti(resFloorWall, resFloorWallOptions) }}</span>
                  <span class="contact-quote__fold-arrow" aria-hidden="true" />
                </summary>
                <div class="contact-quote__fold-panel">
                  <label v-for="opt in resFloorWallOptions" :key="opt.value" class="contact-quote__check">
                    <input v-model="resFloorWall" type="checkbox" :value="opt.value" />
                    {{ opt.label }}
                  </label>
                </div>
              </details>
            </div>

            <div class="contact-quote__field contact-quote__field--full">
              <span class="contact-quote__label">收纳系统（可多选）</span>
              <details class="contact-quote__fold">
                <summary class="contact-quote__fold-summary">
                  <span class="contact-quote__fold-hint">{{ summarizeMulti(resStorage, resStorageOptions) }}</span>
                  <span class="contact-quote__fold-arrow" aria-hidden="true" />
                </summary>
                <div class="contact-quote__fold-panel">
                  <label v-for="opt in resStorageOptions" :key="opt.value" class="contact-quote__check">
                    <input v-model="resStorage" type="checkbox" :value="opt.value" />
                    {{ opt.label }}
                  </label>
                </div>
              </details>
            </div>

            <div class="contact-quote__field contact-quote__field--full">
              <span class="contact-quote__label">家庭智能（可多选）</span>
              <details class="contact-quote__fold">
                <summary class="contact-quote__fold-summary">
                  <span class="contact-quote__fold-hint">{{ summarizeMulti(resSmartHome, resSmartHomeOptions) }}</span>
                  <span class="contact-quote__fold-arrow" aria-hidden="true" />
                </summary>
                <div class="contact-quote__fold-panel">
                  <label v-for="opt in resSmartHomeOptions" :key="opt.value" class="contact-quote__check">
                    <input v-model="resSmartHome" type="checkbox" :value="opt.value" />
                    {{ opt.label }}
                  </label>
                </div>
              </details>
            </div>
          </div>
        </div>

        <div class="contact-quote__section-title contact-quote__section-title--tight">联系方式</div>

        <div class="contact-quote__grid contact-quote__grid--contact">
          <div class="contact-quote__field contact-quote__field--gender">
            <label class="contact-quote__label contact-quote__label--required" for="gender">请告诉我们如何称呼您？</label>
            <div class="contact-quote__gender-row">
            <input
              v-model="lastName"
              class="contact-quote__surname"
              type="text"
              maxlength="4"
              placeholder="请输入您的姓氏"
              aria-label="姓氏"
              aria-required="true"
            />

              <select id="gender" v-model="gender" aria-label="称呼" class="contact-quote__gender">
                <option value="mr">先生</option>
                <option value="ms">女士</option>
              </select>
            </div>
          </div>

          <div class="contact-quote__field">
            <label class="contact-quote__label contact-quote__label--required" for="phone">联系电话</label>
            <input
              id="phone"
              v-model="phone"
              class="contact-quote__phone"
              type="tel"
              maxlength="32"
              autocomplete="tel"
              placeholder="请输入您的联系电话"
              aria-label="联系电话"
              aria-required="true"
            />
          </div>
        </div>

        <div class="contact-quote__field">
          <label class="contact-quote__label" for="remark">备注</label>
          <textarea
            id="remark"
            v-model="remark"
            class="contact-quote__remark"
            rows="4"
            maxlength="4000"
            placeholder="请输入你的备注（可选）"
            aria-label="备注栏"
          />
        </div>

        <div class="contact-quote__actions">
          <button type="submit" class="contact-quote__submit" :disabled="submitting">
            <PaperPlaneIcon class="contact-quote__submit-icon" />
            <span class="contact-quote__submit-text">{{ submitting ? '提交中…' : '获取报价' }}</span>
          </button>
        </div>

        <p v-if="errorText" class="contact-quote__msg contact-quote__msg--error">{{ errorText }}</p>
      </form>

      <div class="contact-quote__unitref">
        <HomePricingSection :show-detail-button="false" />
      </div>

      <div v-if="showSuccessModal" class="contact-quote__modal" role="dialog" aria-modal="true" aria-label="提交成功弹窗">
        <div class="contact-quote__modal-card">
          <div class="contact-quote__modal-title">提交成功</div>
          <div class="contact-quote__modal-body">
            感谢您的信任，我们的总工程师将根据您的信息尽快联系您！
          </div>
          <button type="button" class="contact-quote__modal-close" @click="showSuccessModal = false">关闭</button>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'

import { submitQuoteLead } from '@/api/leads'
import PaperPlaneIcon from '@/components/icons/PaperPlaneIcon.vue'
import HomePricingSection from '@/components/home/HomePricingSection.vue'
import { validatePhone } from '@/utils/phoneValidation'

export type ContactQuoteGender = 'ms' | 'mr'

export type ContactQuotePayload = {
  planKey: 'store' | 'business' | 'residential'
  common: {
    buildingType: string
    schedule: string
  }
  store?: {
    storeType: string
    shopArea: string
    backArea: string
    doorSignNeeds: string[]
    specialDevices: string[]
    licenseAssist: string
  }
  business?: {
    businessSeatArea: string
    businessOfficeCount: string
    businessMeetingCount: string
    businessFuncZones: string[]
    businessSoundproof: string
    businessWeakElectrics: string[]
    businessAcType: string
    businessFurnitureCustomized: string
  }
  residential?: {
    resHomeArea: string
    resBedroomCount: string
    resBathroomCount: string
    resLivingRoomCount: string
    resDiningRoomCount: string
    resKeyAreas: string[]
    resIslandNeed: string
    resFloorWall: string[]
    resStorage: string[]
    resSmartHome: string[]
  }
  contact: {
    gender: ContactQuoteGender
    lastName: string
    phone: string
    remark: string
  }
}

const emit = defineEmits<{
  submit: [payload: ContactQuotePayload]
}>()

const selectedPlan = ref<ContactQuotePayload['planKey']>('store')

type MultiOpt = { value: string; label: string }

const doorSignOptions: MultiOpt[] = [
  { value: 'light', label: '发光字' },
  { value: 'window', label: '橱窗设计' },
  { value: 'sunshelter', label: '遮阳棚' },
  { value: 'other', label: '其他' },
]

const specialDeviceOptions: MultiOpt[] = [
  { value: 'high-power', label: '大功率用电' },
  { value: 'water-elec', label: '水电改造' },
  { value: 'ac', label: '空调' },
  { value: 'cctv', label: '监控' },
  { value: 'fire-safety', label: '消防（喷淋、安全出口、灭火器）' },
  { value: 'other', label: '其他' },
]

const businessFuncZoneOptions: MultiOpt[] = [
  { value: 'front', label: '前台' },
  { value: 'tea', label: '茶水间' },
  { value: 'server', label: '机房' },
  { value: 'rest', label: '休息室' },
  { value: 'other', label: '其他' },
]

const businessWeakElectricOptions: MultiOpt[] = [
  { value: 'network', label: '网络布线' },
  { value: 'access-control', label: '门禁系统' },
  { value: 'video-meeting', label: '视频会议系统' },
  { value: 'bgm', label: '背景音乐' },
  { value: 'other', label: '其他' },
]


const resFloorWallOptions: MultiOpt[] = [
  { value: 'wood-floor', label: '实木地板' },
  { value: 'composite-floor', label: '复合地板' },
  { value: 'tile', label: '瓷砖' },
  { value: 'panel', label: '护墙板定制' },
  { value: 'art-paint', label: '艺术漆' },
  { value: 'wallpaper', label: '壁纸' },
  { value: 'other', label: '其他' },
]

const resStorageOptions: MultiOpt[] = [
  { value: 'wardrobe', label: '步入式衣帽间' },
  { value: 'shoe-cabinet', label: '嵌入式鞋柜' },
  { value: 'bookcase', label: '书柜定制' },
  { value: 'other', label: '其他' },
]

const resSmartHomeOptions: MultiOpt[] = [
  { value: 'smart-light', label: '全屋智能灯光' },
  { value: 'underfloor-heating', label: '地暖系统' },
  { value: 'water-purifier', label: '中央净水' },
  { value: 'other', label: '其他' },
]

function summarizeMulti(selected: string[], options: MultiOpt[]): string {
  if (selected.length === 0) return '请选择'
  return selected
    .map((v) => options.find((o) => o.value === v)?.label ?? v)
    .join('、')
}

// 通用
const buildingType = ref('')
const schedule = ref('')

// 店铺
const storeType = ref('')
const shopArea = ref('')
const backArea = ref('')
const doorSignNeeds = ref<string[]>([])
const specialDevices = ref<string[]>([])
const licenseAssist = ref('')

// 商务
const businessSeatArea = ref('')
const businessOfficeCount = ref('')
const businessMeetingCount = ref('')
const businessFuncZones = ref<string[]>([])
const businessSoundproof = ref('')
const businessWeakElectrics = ref<string[]>([])
const businessAcType = ref('')
const businessFurnitureCustomized = ref('')

// 家装
const resHomeArea = ref('')
const resBedroomCount = ref('')
const resBathroomCount = ref('')
const resLivingRoomCount = ref('')
const resDiningRoomCount = ref('')
const resKeyAreas = ref<string[]>([])
const resIslandNeed = ref('')
const resFloorWall = ref<string[]>([])
const resStorage = ref<string[]>([])
const resSmartHome = ref<string[]>([])

const gender = ref<ContactQuotePayload['contact']['gender']>('mr')
const lastName = ref('')
const phone = ref('')
const remark = ref('')

const errorText = ref('')
const showSuccessModal = ref(false)
const submitting = ref(false)

const planList = computed(() => [
  {
    key: 'store' as const,
    title: '品牌店装',
  },
  {
    key: 'business' as const,
    title: '商务·办公',
  },
  {
    key: 'residential' as const,
    title: '精品家装',
  },
])

function validateRequired(): string | null {
  if (!buildingType.value) return '请先选择建筑类型'
  if (!schedule.value) return '请先选择预计工期'

  if (selectedPlan.value === 'store') {
    if (!storeType.value) return '请先选择店铺类型'
    if (!shopArea.value) return '请先选择门店营业面积'
  }

  if (selectedPlan.value === 'business') {
    if (!businessSeatArea.value) return '请先选择工程面积'
  }

  if (selectedPlan.value === 'residential') {
    if (!resHomeArea.value) return '请先选择房屋面积'
  }

  const ln = lastName.value.trim()
  const ph = phone.value.trim()
  if (!ln) return '请填写您的姓氏'
  if (!validatePhone(ph)) return '请填写正确的联系电话（手机号）'

  return null
}

async function onSubmit() {
  if (submitting.value) return
  errorText.value = ''
  showSuccessModal.value = false

  const requiredError = validateRequired()
  if (requiredError) {
    errorText.value = requiredError
    return
  }

  const ln = lastName.value.trim()
  const ph = phone.value.trim()

  const payload: ContactQuotePayload = {
    planKey: selectedPlan.value,
    common: {
      buildingType: buildingType.value,
      schedule: schedule.value,
    },
    ...(selectedPlan.value === 'store'
      ? {
          store: {
            storeType: storeType.value,
            shopArea: shopArea.value,
            backArea: backArea.value,
            doorSignNeeds: doorSignNeeds.value,
            specialDevices: specialDevices.value,
            licenseAssist: licenseAssist.value,
          },
        }
      : {}),
    ...(selectedPlan.value === 'business'
      ? {
          business: {
            businessSeatArea: businessSeatArea.value,
            businessOfficeCount: businessOfficeCount.value,
            businessMeetingCount: businessMeetingCount.value,
            businessFuncZones: businessFuncZones.value,
            businessSoundproof: businessSoundproof.value,
            businessWeakElectrics: businessWeakElectrics.value,
            businessAcType: businessAcType.value,
            businessFurnitureCustomized: businessFurnitureCustomized.value,
          },
        }
      : {}),
    ...(selectedPlan.value === 'residential'
      ? {
          residential: {
            resHomeArea: resHomeArea.value,
            resBedroomCount: resBedroomCount.value,
            resBathroomCount: resBathroomCount.value,
            resLivingRoomCount: resLivingRoomCount.value,
            resDiningRoomCount: resDiningRoomCount.value,
            resKeyAreas: resKeyAreas.value,
            resIslandNeed: resIslandNeed.value,
            resFloorWall: resFloorWall.value,
            resStorage: resStorage.value,
            resSmartHome: resSmartHome.value,
          },
        }
      : {}),
    contact: {
      gender: gender.value,
      lastName: ln,
      phone: ph,
      remark: remark.value.trim(),
    },
  }

  submitting.value = true
  try {
    await submitQuoteLead(payload)
    emit('submit', payload)
    showSuccessModal.value = true
  } catch (e) {
    errorText.value = e instanceof Error ? e.message : '提交失败，请稍后重试'
  } finally {
    submitting.value = false
  }
}
</script>

<style scoped>
.contact-quote {
  padding: 1.75rem 0 2.25rem;
  background: transparent;
}

.contact-quote__wrap {
  width: 100%;
  max-width: 1200px;
  margin-left: auto;
  margin-right: auto;
  padding: 0 1.5rem;
  box-sizing: border-box;
}

@media (max-width: 480px) {
  .contact-quote__wrap {
    padding: 0 1rem;
  }
}

.contact-quote__title {
  margin: 0 0 1.75rem;
  font-size: clamp(1.6rem, 2.2vw + 1rem, 2.4rem);
  font-weight: 900;
  letter-spacing: -0.03em;
  text-align: center;
}

.contact-quote__plans {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 1.25rem;
}

@media (max-width: 767px) {
  .contact-quote__plans {
    grid-template-columns: 1fr;
  }
}

.contact-plan {
  appearance: none;
  width: 100%;
  border: none;
  text-align: left;
  padding: 1.2rem 1.25rem;
  background: #f1f1f1;
  border-radius: 10px;
  cursor: pointer;
  transition: transform 0.15s ease, box-shadow 0.15s ease, background 0.15s ease;
}

.contact-plan:hover {
  transform: translateY(-1px);
  box-shadow: 0 10px 26px rgb(0 0 0 / 0.08);
}

.contact-plan--active {
  background: #e6e6e6;
  box-shadow: inset 0 0 0 2px rgba(0, 0, 0, 0.08);
}

.contact-plan__title {
  font-size: 1rem;
  font-weight: 800;
  color: #111;
  text-align: center;
}

.contact-quote__form {
  margin-top: 1.25rem;
  padding: 1.25rem 0 0.5rem;
}

.contact-quote__section-title {
  margin: 1.25rem 0 0.75rem;
  font-weight: 900;
  letter-spacing: -0.02em;
  font-size: 1rem;
}

.contact-quote__section-title--tight {
  margin-top: 1.75rem;
}

.contact-quote__plan-block {
  margin-top: 0.25rem;
}

.contact-quote__grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 1rem;
}

.contact-quote__grid--contact {
  grid-template-columns: 1fr 1fr;
}

/* 平板：表单双列；手机：单列 */
@media (max-width: 980px) and (min-width: 768px) {
  .contact-quote__grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 767px) {
  .contact-quote__grid,
  .contact-quote__grid--contact {
    grid-template-columns: 1fr;
  }
}

.contact-quote__field {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.contact-quote__label {
  font-size: 0.85rem;
  color: rgba(0, 0, 0, 0.65);
}

.contact-quote__label--required::before {
  content: '* ';
  color: #c62828;
  font-weight: 700;
}

.contact-quote__field--full {
  grid-column: 1 / -1;
}

.contact-quote__fold {
  border-radius: 12px;
  background: #f1f1f1;
  overflow: hidden;
}

.contact-quote__fold-summary {
  cursor: pointer;
  list-style: none;
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 0.6rem;
  min-height: 44px;
  padding: 0.6rem 0.75rem 0.6rem 0.9rem;
  box-sizing: border-box;
}

.contact-quote__fold-summary::-webkit-details-marker {
  display: none;
}

.contact-quote__fold-hint {
  flex: 1;
  min-width: 0;
  font-size: 0.9rem;
  color: rgba(0, 0, 0, 0.75);
  text-align: left;
  line-height: 1.45;
  word-break: break-word;
}

.contact-quote__fold-arrow {
  flex-shrink: 0;
  width: 10px;
  height: 10px;
  margin-top: 0.42rem;
  border-left: 2px solid rgba(0, 0, 0, 0.55);
  border-bottom: 2px solid rgba(0, 0, 0, 0.55);
  transform: rotate(-45deg);
  transition: transform 0.15s ease;
  pointer-events: none;
}

.contact-quote__fold[open] > .contact-quote__fold-summary .contact-quote__fold-arrow {
  margin-top: 0.28rem;
  transform: rotate(135deg);
}

.contact-quote__fold-panel {
  padding: 0 0.9rem 0.85rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  border-top: 1px solid rgba(0, 0, 0, 0.06);
}

.contact-quote__check {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
  color: rgba(0, 0, 0, 0.85);
  cursor: pointer;
}

.contact-quote__check input {
  width: 1rem;
  height: 1rem;
  flex-shrink: 0;
}

.contact-quote__select {
  position: relative;
}

.contact-quote__select select {
  width: 100%;
  height: 44px;
  border-radius: 12px;
  border: none;
  outline: none;
  padding: 0 2.1rem 0 0.9rem;
  background: #f1f1f1;
  color: rgba(0, 0, 0, 0.85);
  font-size: 0.9rem;
  appearance: none;
  box-sizing: border-box;
}

.contact-quote__select-arrow {
  position: absolute;
  right: 0.9rem;
  top: 50%;
  width: 10px;
  height: 10px;
  border-left: 2px solid rgba(0, 0, 0, 0.55);
  border-bottom: 2px solid rgba(0, 0, 0, 0.55);
  transform: translateY(-60%) rotate(-45deg);
  pointer-events: none;
}

.contact-quote__gender-row {
  display: grid;
  grid-template-columns: 1fr 90px;
  gap: 0.75rem;
  align-items: center;
}

.contact-quote__gender {
  height: 44px;
  border-radius: 12px;
  border: none;
  outline: none;
  background: #f1f1f1;
  color: rgba(0, 0, 0, 0.85);
  font-size: 0.9rem;
  padding: 0 0.35rem;
  box-sizing: border-box;
  text-align: center;
  text-align-last: center;
}

.contact-quote__surname {
  height: 44px;
  border-radius: 12px;
  border: none;
  outline: none;
  background: #f1f1f1;
  color: rgba(0, 0, 0, 0.85);
  font-size: 0.9rem;
  padding: 0 1.15rem;
  box-sizing: border-box;
}

.contact-quote__surname::placeholder {
  color: rgba(0, 0, 0, 0.35);
  font-size: 0.95rem;
}

.contact-quote__phone {
  height: 44px;
  border-radius: 12px;
  border: none;
  outline: none;
  background: #f1f1f1;
  color: rgba(0, 0, 0, 0.85);
  font-size: 0.9rem;
  padding: 0 1.15rem;
  box-sizing: border-box;
}

.contact-quote__phone::placeholder {
  color: rgba(0, 0, 0, 0.35);
  font-size: 0.95rem;
}

.contact-quote__remark {
  width: 100%;
  border-radius: 12px;
  border: none;
  outline: none;
  background: #f1f1f1;
  color: rgba(0, 0, 0, 0.85);
  font-size: 0.9rem;
  padding: 0.85rem 1.15rem;
  box-sizing: border-box;
  resize: vertical;
}

.contact-quote__remark::placeholder {
  color: rgba(0, 0, 0, 0.35);
  font-size: 0.95rem;
}

.contact-quote__actions {
  margin-top: 1.75rem;
  display: flex;
  justify-content: center;
}

.contact-quote__unitref {
  margin-top: 2rem;
}

:deep(.contact-quote__unitref .home-pricing) {
  padding-top: 0.25rem;
  padding-bottom: 0;
}

.contact-quote__submit {
  height: 44px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.6rem;
  border: none;
  border-radius: 999px;
  background: #ff5449;
  color: #fff;
  cursor: pointer;
  padding: 0 1.3rem;
}

.contact-quote__submit:disabled {
  opacity: 0.65;
  cursor: not-allowed;
}

.contact-quote__submit-icon {
  width: 1.1rem;
  height: 1.1rem;
  flex-shrink: 0;
}

.contact-quote__submit-text {
  font-size: 1rem;
  font-weight: 800;
  letter-spacing: -0.01em;
  white-space: nowrap;
}

.contact-quote__msg {
  margin-top: 0.75rem;
  font-size: 0.9rem;
  line-height: 1.35;
  text-align: center;
}

.contact-quote__msg--error {
  color: #c41e3a;
}

.contact-quote__modal {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.45);
  z-index: 999;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1.25rem;
  box-sizing: border-box;
}

.contact-quote__modal-card {
  width: 100%;
  max-width: 520px;
  background: #fff;
  border-radius: 16px;
  padding: 1.25rem 1.25rem 1rem;
  box-sizing: border-box;
  box-shadow: 0 20px 50px rgb(0 0 0 / 0.2);
}

.contact-quote__modal-title {
  font-weight: 900;
  letter-spacing: -0.02em;
  font-size: 1.1rem;
}

.contact-quote__modal-body {
  margin-top: 0.75rem;
  font-size: 0.95rem;
  color: rgba(0, 0, 0, 0.8);
  line-height: 1.6;
}

.contact-quote__modal-close {
  margin-top: 1.1rem;
  height: 42px;
  width: 100%;
  border-radius: 999px;
  border: none;
  cursor: pointer;
  background: #111;
  color: #fff;
  font-weight: 800;
  font-size: 0.95rem;
}
</style>

