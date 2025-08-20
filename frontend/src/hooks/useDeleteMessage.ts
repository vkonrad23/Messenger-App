import { useMutation, useQueryClient } from '@tanstack/react-query'
import { api } from '../lib/api'

export function useDeleteMessage(threadId: string) {
  const qc = useQueryClient()

  const deleteMessage = async (id: string) => {
    const res = await api.delete(`/messages/${id}`)
    if (res.status !== 200 && res.status !== 204) {
      throw new Error('Failed to delete')
    }
    return id
  }

  return useMutation<string, unknown, string>({
    mutationFn: deleteMessage,
    onSuccess: (deletedId: string) => {
      // Simple paged list
      qc.setQueryData<{ id: string }[] | undefined>(['messages', threadId], (old: { id: string }[] | undefined) => {
        const list = old ?? []
        return list.filter((m) => m.id !== deletedId)
      })

      // InfiniteQuery shape
      const dropFromPage = (page: any) => ({
        ...page,
        items: page.items.filter((m: { id: string }) => m.id !== deletedId),
      })

      qc.setQueryData<any>(['messages', threadId, 'infinite'], (old: any) => {
        if (!old) return old
        return {
          ...old,
          pages: old.pages.map(dropFromPage),
        }
      })
    },
  })
}
