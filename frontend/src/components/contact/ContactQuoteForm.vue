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
            <label class="contact-quote__label" for="building-type">建筑类型（新建/翻新）</label>
            <div class="contact-quote__select">
              <select id="building-type" v-model="buildingType" aria-label="建筑类型">
                <option disabled value="">请选择</option>
                <option value="new">新建</option>
                <option value="renovation">翻新</option>
                <option value="other">其他</option>
              </select>
              <span class="contact-quote__select-arrow" aria-hidden="true" />
            </div>
          </div>

          <div class="contact-quote__field">
            <label class="contact-quote__label" for="schedule">预计工期（1月-3月）</label>
            <div class="contact-quote__select">
              <select id="schedule" v-model="schedule" aria-label="预计工期">
                <option disabled value="">请选择</option>
                <option value="1-3">1月-3月</option>
                <option value="4-6">4月-6月</option>
                <option value="7-9">7月-9月</option>
                <option value="10-12">10月-12月</option>
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
              <label class="contact-quote__label" for="store-type">店铺类型（餐饮/零售/美容美发/健身房）</label>
              <div class="contact-quote__select">
                <select id="store-type" v-model="storeType" aria-label="店铺类型">
                  <option disabled value="">请选择</option>
                  <option value="food">餐饮</option>
                  <option value="retail">零售</option>
                  <option value="beauty">美容美发</option>
                  <option value="fitness">健身房</option>
                  <option value="other">其他</option>
                </select>
                <span class="contact-quote__select-arrow" aria-hidden="true" />
              </div>
            </div>

            <div class="contact-quote__field">
              <label class="contact-quote__label" for="shop-area">门店面积（营业面积）</label>
              <div class="contact-quote__select">
                <select id="shop-area" v-model="shopArea" aria-label="营业面积">
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

            <div class="contact-quote__field">
              <label class="contact-quote__label" for="door-sign">门头需求（是否需要发光字/橱窗设计/遮阳棚）</label>
              <select id="door-sign" v-model="doorSignNeeds" class="contact-quote__multi" multiple aria-label="门头需求">
                <option value="light">发光字</option>
                <option value="window">橱窗设计</option>
                <option value="sunshelter">遮阳棚</option>
                <option value="other">其他</option>
              </select>
            </div>

            <div class="contact-quote__field">
              <label class="contact-quote__label" for="special-devices">特殊设备（大功率用电/水电改造）</label>
              <select id="special-devices" v-model="specialDevices" class="contact-quote__multi" multiple aria-label="特殊设备">
                <option value="high-power">大功率用电</option>
                <option value="water-elec">水电改造</option>
                <option value="other">其他</option>
              </select>
            </div>

            <div class="contact-quote__field">
              <label class="contact-quote__label" for="license-assist">营业执照协助（代办建筑许可/消防）</label>
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
              <label class="contact-quote__label" for="work-area">工位面积</label>
              <div class="contact-quote__select">
                <select id="work-area" v-model="businessSeatArea" aria-label="工位面积">
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
                  <option disabled value="">请选择</option>
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

            <div class="contact-quote__field">
              <label class="contact-quote__label" for="func-zone">功能分区（前台/茶水间/机房/休息室）</label>
              <select id="func-zone" v-model="businessFuncZones" class="contact-quote__multi" multiple aria-label="功能分区">
                <option value="front">前台</option>
                <option value="tea">茶水间</option>
                <option value="server">机房</option>
                <option value="rest">休息室</option>
                <option value="other">其他</option>
              </select>
            </div>

            <div class="contact-quote__field">
              <label class="contact-quote__label" for="soundproof">是否需要隔音处理</label>
              <div class="contact-quote__select">
                <select id="soundproof" v-model="businessSoundproof" aria-label="隔音处理">
                  <option disabled value="">请选择</option>
                  <option value="yes">需要</option>
                  <option value="no">不需要</option>
                  <option value="other">其他</option>
                </select>
                <span class="contact-quote__select-arrow" aria-hidden="true" />
              </div>
            </div>

            <div class="contact-quote__field">
              <label class="contact-quote__label" for="weak-electric">智能化弱电（网络布线/门禁系统/视频会议系统/背景音乐）</label>
              <select id="weak-electric" v-model="businessWeakElectrics" class="contact-quote__multi" multiple aria-label="智能化弱电">
                <option value="network">网络布线</option>
                <option value="access-control">门禁系统</option>
                <option value="video-meeting">视频会议系统</option>
                <option value="bgm">背景音乐</option>
                <option value="other">其他</option>
              </select>
            </div>

            <div class="contact-quote__field">
              <label class="contact-quote__label" for="ac-type">空调系统</label>
              <div class="contact-quote__select">
                <select id="ac-type" v-model="businessAcType" aria-label="空调系统">
                  <option disabled value="">请选择</option>
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
                  <option disabled value="">请选择</option>
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
              <label class="contact-quote__label" for="home-type">房型（几卧/几卫/几客）</label>
              <div class="contact-quote__select">
                <select id="home-type" v-model="resHomeType" aria-label="房型">
                  <option disabled value="">请选择</option>
                  <option value="2-1-1">2卧1卫1客</option>
                  <option value="3-2-1">3卧2卫1客</option>
                  <option value="4-3-2">4卧3卫2客</option>
                  <option value="other">其他</option>
                </select>
                <span class="contact-quote__select-arrow" aria-hidden="true" />
              </div>
            </div>

            <div class="contact-quote__field">
              <label class="contact-quote__label" for="key-areas">重点区域（多选）</label>
              <select id="key-areas" v-model="resKeyAreas" class="contact-quote__multi" multiple aria-label="重点区域">
                <option value="whole">全屋翻新</option>
                <option value="kitchen">厨房改造</option>
                <option value="bathroom">卫生间翻新</option>
                <option value="basement">地下室装修</option>
                <option value="other">其他</option>
              </select>
            </div>

            <div class="contact-quote__field">
              <label class="contact-quote__label" for="cabinet">厨卫细节（橱柜材质）</label>
              <div class="contact-quote__select">
                <select id="cabinet" v-model="resCabinetMaterial" aria-label="橱柜材质">
                  <option disabled value="">请选择</option>
                  <option value="wood">实木</option>
                  <option value="lacquer">烤漆</option>
                  <option value="other">其他</option>
                </select>
                <span class="contact-quote__select-arrow" aria-hidden="true" />
              </div>
            </div>

            <div class="contact-quote__field">
              <label class="contact-quote__label" for="island">岛台需求</label>
              <div class="contact-quote__select">
                <select id="island" v-model="resIslandNeed" aria-label="岛台需求">
                  <option disabled value="">请选择</option>
                  <option value="yes">需要</option>
                  <option value="no">不需要</option>
                  <option value="other">其他</option>
                </select>
                <span class="contact-quote__select-arrow" aria-hidden="true" />
              </div>
            </div>

            <div class="contact-quote__field">
              <label class="contact-quote__label" for="toilet">智能马桶</label>
              <div class="contact-quote__select">
                <select id="toilet" v-model="resSmartToilet" aria-label="智能马桶">
                  <option disabled value="">请选择</option>
                  <option value="yes">需要</option>
                  <option value="no">不需要</option>
                  <option value="other">其他</option>
                </select>
                <span class="contact-quote__select-arrow" aria-hidden="true" />
              </div>
            </div>

            <div class="contact-quote__field">
              <label class="contact-quote__label" for="shower">恒温花洒</label>
              <div class="contact-quote__select">
                <select id="shower" v-model="resThermostaticShower" aria-label="恒温花洒">
                  <option disabled value="">请选择</option>
                  <option value="yes">需要</option>
                  <option value="no">不需要</option>
                  <option value="other">其他</option>
                </select>
                <span class="contact-quote__select-arrow" aria-hidden="true" />
              </div>
            </div>

            <div class="contact-quote__field">
              <label class="contact-quote__label" for="floor-wall">地板墙面（多选）</label>
              <select id="floor-wall" v-model="resFloorWall" class="contact-quote__multi" multiple aria-label="地板墙面">
                <option value="wood-floor">实木地板</option>
                <option value="composite-floor">复合地板</option>
                <option value="panel">护墙板定制</option>
                <option value="art-paint">艺术漆</option>
                <option value="wallpaper">壁纸</option>
                <option value="other">其他</option>
              </select>
            </div>

            <div class="contact-quote__field">
              <label class="contact-quote__label" for="storage">收纳系统（多选）</label>
              <select id="storage" v-model="resStorage" class="contact-quote__multi" multiple aria-label="收纳系统">
                <option value="wardrobe">步入式衣帽间</option>
                <option value="shoe-cabinet">嵌入式鞋柜</option>
                <option value="bookcase">书柜定制</option>
                <option value="other">其他</option>
              </select>
            </div>

            <div class="contact-quote__field">
              <label class="contact-quote__label" for="smart-home">家庭智能（多选）</label>
              <select id="smart-home" v-model="resSmartHome" class="contact-quote__multi" multiple aria-label="家庭智能">
                <option value="smart-light">全屋智能灯光</option>
                <option value="underfloor-heating">地暖系统</option>
                <option value="water-purifier">中央净水</option>
                <option value="other">其他</option>
              </select>
            </div>
          </div>
        </div>

        <div class="contact-quote__section-title contact-quote__section-title--tight">联系方式</div>

        <div class="contact-quote__grid contact-quote__grid--contact">
          <div class="contact-quote__field contact-quote__field--gender">
            <label class="contact-quote__label" for="gender">请告诉我们如何称呼您？</label>
            <div class="contact-quote__gender-row">
              <input
                v-model="lastName"
                class="contact-quote__surname"
                type="text"
                maxlength="4"
                placeholder="请输入您的姓氏"
                aria-label="姓氏"
              />

              <select id="gender" v-model="gender" aria-label="称呼" class="contact-quote__gender">
                <option value="mr">先生</option>
                <option value="ms">女士</option>
              </select>
              
            </div>
          </div>

          <div class="contact-quote__field">
            <label class="contact-quote__label" for="phone">联系电话</label>
            <input
              id="phone"
              v-model="phone"
              class="contact-quote__phone"
              type="tel"
              placeholder="请输入您的联系电话"
              aria-label="联系电话"
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
            placeholder="请输入你的备注（可选）"
            aria-label="备注栏"
          />
        </div>

        <div class="contact-quote__actions">
          <button type="submit" class="contact-quote__submit">
            <PaperPlaneIcon class="contact-quote__submit-icon" />
            <span class="contact-quote__submit-text">获取报价</span>
          </button>
        </div>

        <p v-if="errorText" class="contact-quote__msg contact-quote__msg--error">{{ errorText }}</p>
      </form>

      <!-- 表单下方：参考单价（装修单价） -->
      <div class="contact-quote__unitref">
        <ContactUnitPriceReference :plans="unitPricePlans" :active-key="selectedPlan" />
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

import PaperPlaneIcon from '@/components/icons/PaperPlaneIcon.vue'
import ContactUnitPriceReference, { type ContactUnitRefPlan } from './ContactUnitPriceReference.vue'

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
    resHomeType: string
    resKeyAreas: string[]
    resCabinetMaterial: string
    resIslandNeed: string
    resSmartToilet: string
    resThermostaticShower: string
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
const resHomeType = ref('')
const resKeyAreas = ref<string[]>([])
const resCabinetMaterial = ref('')
const resIslandNeed = ref('')
const resSmartToilet = ref('')
const resThermostaticShower = ref('')
const resFloorWall = ref<string[]>([])
const resStorage = ref<string[]>([])
const resSmartHome = ref<string[]>([])

const gender = ref<ContactQuotePayload['contact']['gender']>('mr')
const lastName = ref('')
const phone = ref('')
const remark = ref('')

const errorText = ref('')
const showSuccessModal = ref(false)

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

const unitPricePlans = computed<ContactUnitRefPlan[]>(() => [
  {
    key: 'store',
    title: '品牌店装',
    unitPrice: 20,
    bullets: ['预算规划与空间落地建议', '关键工艺与材料清单梳理', '后续交付与验收重点提醒'],
  },
  {
    key: 'business',
    title: '商务·办公',
    unitPrice: 60,
    bullets: ['功能分区与动线优化建议', '弱电/空调对接方案要点', '施工进度与验收流程提醒'],
  },
  {
    key: 'residential',
    title: '精品家装',
    unitPrice: 120,
    bullets: ['房型结构与重点区域方案要点', '材料与细节做法建议', '交付时间与质保事项说明'],
  },
])

function validatePhone(v: string) {
  // 简单校验：允许 +86 / 0 前缀的 6~15 位数字
  return /^[+]?(\d){5,15}$/.test(v.replace(/\s+/g, '')) || /^0\d{5,14}$/.test(v)
}

function validateRequired(): string | null {
  if (!buildingType.value) return '请先选择建筑类型'
  if (!schedule.value) return '请先选择预计工期'

  if (selectedPlan.value === 'store') {
    if (!storeType.value) return '请先选择店铺类型'
    if (!shopArea.value) return '请先选择营业面积'
    if (!backArea.value) return '请先选择后厨/仓库面积'
    if (doorSignNeeds.value.length === 0) return '请先选择门头需求'
    if (specialDevices.value.length === 0) return '请先选择特殊设备'
    if (!licenseAssist.value) return '请先选择营业执照协助'
  }

  if (selectedPlan.value === 'business') {
    if (!businessSeatArea.value) return '请先选择工位面积'
    if (!businessOfficeCount.value) return '请先选择独立办公室数量'
    if (!businessMeetingCount.value) return '请先选择会议室数量'
    if (businessFuncZones.value.length === 0) return '请先选择功能分区'
    if (!businessSoundproof.value) return '请先选择隔音处理'
    if (businessWeakElectrics.value.length === 0) return '请先选择智能化弱电'
    if (!businessAcType.value) return '请先选择空调系统'
    if (!businessFurnitureCustomized.value) return '请先选择家具定制'
  }

  if (selectedPlan.value === 'residential') {
    if (!resHomeType.value) return '请先选择房型'
    if (resKeyAreas.value.length === 0) return '请先选择重点区域'
    if (!resCabinetMaterial.value) return '请先选择橱柜材质'
    if (!resIslandNeed.value) return '请先选择岛台需求'
    if (!resSmartToilet.value) return '请先选择智能马桶需求'
    if (!resThermostaticShower.value) return '请先选择恒温花洒需求'
    if (resFloorWall.value.length === 0) return '请先选择地板墙面'
    if (resStorage.value.length === 0) return '请先选择收纳系统'
    if (resSmartHome.value.length === 0) return '请先选择家庭智能'
  }

  const ln = lastName.value.trim()
  const ph = phone.value.trim()
  if (!ln) return '请填写您的姓氏'
  if (!validatePhone(ph)) return '请填写正确的联系电话（手机号）'

  return null
}

function onSubmit() {
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
            resHomeType: resHomeType.value,
            resKeyAreas: resKeyAreas.value,
            resCabinetMaterial: resCabinetMaterial.value,
            resIslandNeed: resIslandNeed.value,
            resSmartToilet: resSmartToilet.value,
            resThermostaticShower: resThermostaticShower.value,
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

  emit('submit', payload)

  // TODO: 接入后端（暂时不做真实请求）
  // await fetch('/api/contact/quote', { method:'POST', body: JSON.stringify(payload) })

  showSuccessModal.value = true
}
</script>

<style scoped>
.contact-quote {
  padding: 1.75rem 0 2.25rem;
  background: transparent;
}

.contact-quote__wrap {
  width: 100%;
  max-width: 1080px;
  margin-left: auto;
  margin-right: auto;
  padding: 0 1.5rem;
  box-sizing: border-box;
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

@media (max-width: 980px) {
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

@media (max-width: 980px) {
  .contact-quote__grid {
    grid-template-columns: 1fr;
  }

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

.contact-quote__multi {
  width: 100%;
  min-height: 120px;
  border-radius: 12px;
  border: none;
  outline: none;
  padding: 0.75rem 0.9rem;
  background: #f1f1f1;
  color: rgba(0, 0, 0, 0.85);
  font-size: 0.9rem;
  box-sizing: border-box;
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
  padding: 0 0.75rem;
  box-sizing: border-box;
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

