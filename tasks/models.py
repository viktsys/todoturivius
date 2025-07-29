from django.db import models
from django.utils import timezone


class Task(models.Model):
    """
    Modelo para representar uma tarefa na lista de tarefas.
    """
    title = models.CharField(
        max_length=200,
        verbose_name="Título",
        help_text="Título da tarefa"
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Descrição",
        help_text="Descrição detalhada da tarefa"
    )
    completed = models.BooleanField(
        default=False,
        verbose_name="Concluída",
        help_text="Indica se a tarefa foi concluída"
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name="Criada em",
        help_text="Data e hora de criação da tarefa"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Atualizada em",
        help_text="Data e hora da última atualização"
    )

    class Meta:
        verbose_name = "Tarefa"
        verbose_name_plural = "Tarefas"
        ordering = ['-created_at']  # Ordenar por data de criação, mais recentes primeiro

    def __str__(self):
        return self.title

    def toggle_completed(self):
        """
        Alterna o status de conclusão da tarefa.
        """
        self.completed = not self.completed
        self.save()
        return self.completed
