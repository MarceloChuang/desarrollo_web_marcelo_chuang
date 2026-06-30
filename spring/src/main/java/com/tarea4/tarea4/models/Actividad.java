package com.tarea4.tarea4.models;

import jakarta.persistence.*;

@Entity
@Table(name = "actividad")
public class Actividad {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    private String nombre;

    @Column(columnDefinition = "TEXT")
    private String descripcion;

    private String tipo;

    private String dias;

    @Column(name = "hora_inicio")
    private String horaInicio;

    @Column(name = "hora_termino")
    private String horaTermino;

    private String enlace;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "miembro_id")
    private Miembro miembro;

    public Integer getId() {
        return id;
    }

    public String getNombre() {
        return nombre;
    }

    public String getDescripcion() {
        return descripcion;
    }

    public String getTipo() {
        return tipo;
    }

    public String getDias() {
        return dias;
    }

    public String getHoraInicio() {
        return horaInicio;
    }

    public String getHoraTermino() {
        return horaTermino;
    }

    public String getEnlace() {
        return enlace;
    }

    public Miembro getMiembro() {
        return miembro;
    }
}