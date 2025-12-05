import { create } from 'zustand'
import { Cart, AddCartItemRequest } from '../types'
import { cartApi } from '../api/cart'

interface CartState {
  cart: Cart | null
  loading: boolean
  error: string | null
  fetchCart: () => Promise<void>
  addItem: (data: AddCartItemRequest) => Promise<void>
  updateItem: (id: number, quantity: number) => Promise<void>
  removeItem: (id: number) => Promise<void>
  clearCart: () => Promise<void>
  resetCart: () => void
}

export const useCartStore = create<CartState>((set, get) => ({
  cart: null,
  loading: false,
  error: null,

  fetchCart: async () => {
    set({ loading: true, error: null })
    try {
      const response = await cartApi.getCart()
      if (response.success) {
        // 장바구니가 비어있어도 빈 Cart 객체를 반환하므로 항상 설정
        set({ cart: response.data || null, loading: false })
      } else {
        throw new Error(response.message || '장바구니 조회 실패')
      }
    } catch (error: any) {
      set({ error: error.message || '장바구니 조회 실패', loading: false })
      // 에러 발생 시에도 장바구니를 null로 설정하여 UI 업데이트
      set({ cart: null })
    }
  },

  addItem: async (data: AddCartItemRequest) => {
    set({ loading: true, error: null })
    try {
      // 장바구니 상태를 먼저 가져오기 (아직 로드되지 않았을 수 있음)
      let currentCart = get().cart
      if (!currentCart) {
        await get().fetchCart()
        currentCart = get().cart
      }
      
      // 같은 메뉴, 같은 스타일, 같은 customizedQuantities인 항목 찾기
      if (currentCart && currentCart.items.length > 0) {
        const matchingItem = currentCart.items.find(item => {
          // 같은 메뉴인지 확인
          if (item.menu.id !== data.menuId) return false
          
          // 같은 스타일인지 확인
          if (item.selectedStyle !== data.styleType) return false
          
          // 같은 customizedQuantities인지 확인
          const itemQuantities = item.customizedQuantities || {}
          const dataQuantities = data.customizedQuantities || {}
          
          // 키 개수 비교
          const itemKeys = Object.keys(itemQuantities).sort()
          const dataKeys = Object.keys(dataQuantities).sort()
          if (itemKeys.length !== dataKeys.length) return false
          
          // 모든 키와 값이 같은지 확인
          for (const key of itemKeys) {
            if (itemQuantities[key] !== dataQuantities[key]) return false
          }
          
          return true
        })
        
        // 같은 항목이 있으면 수량만 업데이트
        if (matchingItem) {
          const newQuantity = matchingItem.quantity + data.quantity
          await get().updateItem(matchingItem.id, newQuantity)
          return
        }
      }
      
      // 같은 항목이 없으면 새로 추가 (스타일이 다르거나 다른 메뉴인 경우)
      const response = await cartApi.addItem(data)
      if (response.success) {
        await get().fetchCart()
      } else {
        throw new Error(response.message || '장바구니 추가 실패')
      }
    } catch (error: any) {
      set({ error: error.message || '장바구니 추가 실패', loading: false })
      throw error
    }
  },

  updateItem: async (id: number, quantity: number) => {
    set({ loading: true, error: null })
    try {
      const response = await cartApi.updateItem(id, quantity)
      if (response.success) {
        await get().fetchCart()
      } else {
        throw new Error(response.message || '장바구니 수정 실패')
      }
    } catch (error: any) {
      set({ error: error.message || '장바구니 수정 실패', loading: false })
      throw error
    }
  },

  removeItem: async (id: number) => {
    set({ loading: true, error: null })
    try {
      const response = await cartApi.removeItem(id)
      if (response.success) {
        await get().fetchCart()
      } else {
        throw new Error(response.message || '장바구니 삭제 실패')
      }
    } catch (error: any) {
      set({ error: error.message || '장바구니 삭제 실패', loading: false })
      throw error
    }
  },

  clearCart: async () => {
    set({ loading: true, error: null })
    try {
      const response = await cartApi.clearCart()
      if (response.success) {
        await get().fetchCart()
      } else {
        throw new Error(response.message || '장바구니 비우기 실패')
      }
    } catch (error: any) {
      set({ error: error.message || '장바구니 비우기 실패', loading: false })
      throw error
    }
  },

  resetCart: () => {
    // 장바구니를 빈 상태로 초기화 (주문 완료 후 즉시 UI 업데이트)
    set({ cart: { id: 0, items: [], totalPrice: 0 }, loading: false, error: null })
  },
}))

