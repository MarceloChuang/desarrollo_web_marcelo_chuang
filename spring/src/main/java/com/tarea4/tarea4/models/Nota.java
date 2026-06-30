package com.tarea4.tarea4.models;

import jakarta.persistence.*;
import java.time.LocalDateTime;

@Entity
@Table(name = "nota")
public class Nota {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    private Integer valor;

    @Column(nullable = false)
    private LocalDateTime fecha = LocalDateTime.now();

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "actividad_id")
    private Actividad actividad;

    public Nota() {
    }

    public Nota(Actividad actividad, Integer valor) {
        this.actividad = actividad;
        this.valor = valor;
        this.fecha = LocalDateTime.now();
    }

    public Integer getId() {
        return id;
    }

    public Integer getValor() {
        return valor;
    }

    public LocalDateTime getFecha() {
        return fecha;
    }

    public Actividad getActividad() {
        return actividad;
    }
}